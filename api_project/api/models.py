from django.db import models

# Create your models here.
from django.utils import timezone


class Book(models.Model):
    """
    A simple Book model for API demonstration.
    """
    title = models.CharField(
        max_length=200,
        help_text="The title of the book"
    )
    author = models.CharField(
        max_length=100,
        help_text="The author of the book"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        help_text="ISBN number (optional)"
    )
    publication_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date when the book was published"
    )
    pages = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of pages in the book"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this record was last updated"
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author}"

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}')"