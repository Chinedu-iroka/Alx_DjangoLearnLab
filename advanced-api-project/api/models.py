from django.db import models

# Create your models here.

import datetime

# Author model represents a writer with a name.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Book model represents a book written by an author.
# It includes title, publication year, and a ForeignKey to the Author model.
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title