from django.shortcuts import render

# Create your views here.

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, FollowSerializer, UserProfileWithFollowStatusSerializer
from notifications.models import Notification

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Get the token that was created in the serializer
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    
    if user_to_follow == request.user:
        return Response(
            {'error': 'You cannot follow yourself.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if request.user.follow(user_to_follow):

        Notification.create_notification(
            recipient=user_to_follow,
            actor=request.user,
            verb=Notification.FOLLOW
        )
        
        return Response(
            {'message': f'You are now following {user_to_follow.username}.'},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'error': 'You are already following this user.'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    
    if request.user.unfollow(user_to_unfollow):
        return Response(
            {'message': f'You have unfollowed {user_to_unfollow.username}.'},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'error': 'You are not following this user.'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    following_users = request.user.following.all()
    serializer = UserProfileWithFollowStatusSerializer(
        following_users, 
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    following_users = request.user.following.all()
    serializer = UserProfileWithFollowStatusSerializer(
        following_users, 
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    followers = request.user.followers.all()
    serializer = UserProfileWithFollowStatusSerializer(
        followers, 
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_with_follow_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserProfileWithFollowStatusSerializer(user, context={'request': request})
    return Response(serializer.data)


class UserListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    
    def get(self, request):
        users = self.get_queryset()
        serializer = UserProfileWithFollowStatusSerializer(
            users, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)

# Add another view that uses permissions.IsAuthenticated with CustomUser.objects.all()
class UserSearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    
    def get(self, request):
        search_query = request.query_params.get('search', '')
        if search_query:
            users = CustomUser.objects.filter(
                username__icontains=search_query
            ) | CustomUser.objects.filter(
                first_name__icontains=search_query
            ) | CustomUser.objects.filter(
                last_name__icontains=search_query
            )
        else:
            users = CustomUser.objects.all()
        
        serializer = UserProfileWithFollowStatusSerializer(
            users, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)