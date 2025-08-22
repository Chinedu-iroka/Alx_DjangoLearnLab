from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions, status, filters, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from .serializers import (
    LikeSerializer, PostSerializer, PostCreateSerializer, 
    CommentSerializer, CommentCreateSerializer
)
from .pagination import CustomPagination

User = get_user_model()

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(post=post, author=request.user)

        if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb=Notification.COMMENT,
                    content_type_id=ContentType.objects.get_for_model(comment).id,
                    object_id=comment.id
                )
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            return Response(
                {'error': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create notification using Notification.objects.create
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb=Notification.LIKE,
                content_type_id=ContentType.objects.get_for_model(post).id,
                object_id=post.id
            )
        
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        
        # Check if user already liked this post
        # if Like.objects.filter(user=request.user, post=post).exists():
        #     return Response(
        #         {'error': 'You have already liked this post.'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        
        # # Create like
        # like = Like.objects.create(user=request.user, post=post)
        
        # # Create notification if the post author is not the one liking
        # if post.author != request.user:
        #     Notification.create_notification(
        #         recipient=post.author,
        #         actor=request.user,
        #         verb=Notification.LIKE,
        #         target=post
        #     )
        
        # serializer = LikeSerializer(like)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response(
                {'message': 'Post unliked successfully.'},
                status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {'error': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        post = self.get_object()
        likes = post.likes.all()
        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = LikeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        
        # Create notification if the post author is not the comment author
        if comment.post.author != self.request.user:
            Notification.create_notification(
                recipient=comment.post.author,
                actor=self.request.user,
                verb=Notification.COMMENT,
                content_type_id=ContentType.objects.get_for_model(comment).id,
                object_id=comment.id
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    # Get users that the current user is following
    following_users = request.user.following.all()
    
    # Get posts from followed users, ordered by creation date (newest first)
    feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Paginate the results
    paginator = CustomPagination()
    paginated_posts = paginator.paginate_queryset(feed_posts, request)
    
    # Serialize the posts
    serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
    
    return paginator.get_paginated_response(serializer.data)


class PostLikeDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, post_id):
        post = generics.get_object_or_404(Post, pk=post_id)
        like_exists = Like.objects.filter(user=request.user, post=post).exists()
        return Response({'liked': like_exists})