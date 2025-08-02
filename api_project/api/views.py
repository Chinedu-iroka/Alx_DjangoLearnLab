from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    GET /api/books/ - Returns a list of all books in JSON format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """
        Optionally filter the queryset based on query parameters.
        You can extend this method to add search, filtering, etc.
        """
        queryset = Book.objects.all()
        
        # Example: Filter by author if provided in query params
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__icontains=author)
            
        return queryset


class BookListCreate(generics.ListCreateAPIView):
    """
    API view to retrieve list of books or create a new book.
    
    GET /api/books/ - Returns a list of all books
    POST /api/books/ - Creates a new book
    
    This is an alternative to BookList if you want to support both
    listing and creating books in the same endpoint.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to customize the response.
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