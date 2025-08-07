from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

# Serializer for the Book model
# Serializes all fields in the Book model
# Includes custom validation to prevent future publication years

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Includes title, publication_year, author

# Custom validator to ensure publication year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Serializer for the Author model
# Serializes the author's name and includes a nested list of their books

class AuthorSerializer(serializers.ModelSerializer):

    # Nested representation of books using BookSerializer
    # 'books' refers to the related_name defined in the Book model's ForeignKey
    
    books = BookSerializer(many=True, read_only=True)  # 'books' from related_name in model

    class Meta:
        model = Author
        fields = ['name', 'books'] # Only exposes name and related books