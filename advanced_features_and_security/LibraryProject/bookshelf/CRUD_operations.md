## CREATE
from bookshelf.models import Book
b = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
b  # Output: <Book: 1984 by George Orwell>

## RETRIEVE
b = Book.objects.get(title="1984")
print(b.title, b.author, b.publication_year)  # Output: 1984 George Orwell 1949

## UPDATE
b = Book.objects.get(title="1984")
b.title = "Nineteen Eighty-Four"
b.save()
print(b.title)  # Output: Nineteen Eighty-Four

## DELETE
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()
Book.objects.all()  # Output: <QuerySet []>