from bookshelf.models import Book

# Delete the book
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()

# Confirm deletion
Book.objects.all()
# Output: <QuerySet []>