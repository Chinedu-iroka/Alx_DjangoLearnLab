from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book model instances to JSON format and vice versa.
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model
        
        # Alternative: You can explicitly specify fields if needed
        # fields = ['id', 'title', 'author', 'isbn', 'publication_date', 'pages', 'created_at', 'updated_at']
        
        # Make some fields read-only (timestamps shouldn't be modified via API)
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing books (optional).
    You can use this for list views if you want to show fewer fields.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_date']
        read_only_fields = ['id']