import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')  # <-- change this
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# ---------- 1. Query all books by a specific author ----------
author_name = "John Doe"  # Replace with actual name in your DB
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"\nBooks by {author.name}:")
    for book in books_by_author:
        print(f"- {book.title}")
except Author.DoesNotExist:
    print(f"Author '{author_name}' does not exist.")

# ---------- 2. List all books in a specific library ----------
library_name = "Central Library"  # Replace with actual name in your DB
try:
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"\nBooks in {library.name}:")
    for book in books_in_library:
        print(f"- {book.title}")
except Library.DoesNotExist:
    print(f"Library '{library_name}' does not exist.")

# ---------- 3. Retrieve the librarian for a specific library
try:
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    print(f"\nLibrarian for {library.name}: {librarian.name}")
except (Library.DoesNotExist, Librarian.DoesNotExist):
    print(f"Librarian or Library '{library_name}' does not exist.")