from bookshelf.models import Book

# Retrieve the book
b = Book.objects.get(title="1984")
print(b.title, b.author, b.publication_year)
# Output: 1984 George Orwell 1949