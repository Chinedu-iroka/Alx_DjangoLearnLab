from typing import Self
from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets


# class BookList(generics.ListAPIView):
#     """
#     API view to retrieve a list of all books.
    
#     GET /api/books/ - Returns a list of all books in JSON format
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    
    # def get_queryset(self):
    #     """
    #     Optionally filter the queryset based on query parameters.
    #     You can extend this method to add search, filtering, etc.
    #     """
    #     queryset = Book.objects.all()
        
    #     # Example: Filter by author if provided in query params
    #     author = self.request.query_params.get('author', None)
    #     if author is not None:
    #         queryset = queryset.filter(author__icontains=author)
            
    #     return queryset


# class BookListCreate(generics.ListCreateAPIView):
#     """
#     API view to retrieve list of books or create a new book.
    
#     GET /api/books/ - Returns a list of all books
#     POST /api/books/ - Creates a new book
    
#     This is an alternative to BookList if you want to support both
#     listing and creating books in the same endpoint.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    
#     def create(self, request, *args, **kwargs):
#         """
#         Override create method to customize the response.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             {
#                 'message': 'Book created successfully',
#                 'data': serializer.data
#             },
#             status=status.HTTP_201_CREATED,
#             headers=headers
#         )

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling all CRUD operations on Book model.
    
    This ViewSet automatically provides the following actions:
    - list: GET /api/books_all/ - List all books
    - create: POST /api/books_all/ - Create a new book
    - retrieve: GET /api/books_all/{id}/ - Get a specific book by ID
    - update: PUT /api/books_all/{id}/ - Update a specific book
    - partial_update: PATCH /api/books_all/{id}/ - Partially update a book
    - destroy: DELETE /api/books_all/{id}/ - Delete a specific book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
    def get_queryset(self):
        """
        Optionally filter the returned books based on query parameters.
        """
        queryset = Book.objects.all()
        
        # Filter by author
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__icontains=author)
            
        # Filter by title
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
            
        # Filter by publication year
        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(publication_date__year=year)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to provide custom response format.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Book created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to provide custom response format.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'message': 'Book updated successfully',
                'data': serializer.data
            }
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to provide custom response format.
        """
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'Book "{book_title}" deleted successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """
        Custom action to get books by author.
        Usage: GET /api/books_all/by_author/?author=AuthorName
        """
        author = request.query_params.get('author', None)
        if not author:
            return Response(
                {'error': 'Author parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books = Book.objects.filter(author__icontains=author)
        serializer = self.get_serializer(books, many=True)
        return Response({
            'author': author,
            'books': serializer.data,
            'count': books.count()
        })
    
    @action(detail=True, methods=['post'])
    def mark_favorite(self, request, pk=None):
        """
        Custom action to mark a book as favorite.
        Usage: POST /api/books_all/{id}/mark_favorite/
        
        Note: This is just an example. You'd need to add a 'is_favorite' 
        field to your Book model to make this functional.
        """
        book = self.get_object()
        # If you had an is_favorite field:
        # book.is_favorite = True
        # book.save()
        
        return Response({
            'message': f'Book "{book.title}" marked as favorite',
            'book_id': book.id
        })