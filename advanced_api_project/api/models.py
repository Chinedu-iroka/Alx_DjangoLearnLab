from django.db import models

# Create your models here.

# The Author model represents a book author with a name field.
# Each Author can have multiple books associated with them.

class Author(models.Model):
    name = models.CharField(max_length=255) # Stores the author's name

    def __str__(self):
        return self.name   # Human-readable representation

# The Book model represents a book entity.
# Each Book has a title, publication year, and is linked to an Author.

class Book(models.Model):
    title = models.CharField(max_length=255) # Stores the book's title
    publication_year = models.IntegerField() # Stores the year the book was published
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books') # If the author is deleted, all their books are deleted and also 

    def __str__(self):
        return self.title  # Human-readable representation here