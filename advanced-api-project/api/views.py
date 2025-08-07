from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Author
from .serializers import AuthorSerializer
from rest_framework import generics, permissions
from .models import Book
from rest_framework import status
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# APIView to return all authors and their books
class AuthorListView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


class BookListView(generics.ListAPIView):
    """
    GET: Returns a list of all books.
    Accessible to all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Returns details of a single book by ID.
    Accessible to all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book instance.
    Only accessible by authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book by ID.
    Only accessible by authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a book by ID.
    Only accessible by authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateCustomView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        book_id = request.data.get("id")
        if not book_id:
            return Response({"error": "Book ID is required."}, status=400)
        
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class BookDeleteCustomView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        book_id = request.data.get("id")
        if not book_id:
            return Response({"error": "Book ID is required."}, status=400)

        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response({"message": "Book deleted successfully."}, status=204)