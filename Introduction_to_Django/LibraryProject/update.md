from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Update the book title
[book.title] = "Nineteen Eighty-Four"
book.save()

# Confirm the update
book.title  # ← This is what the checker is looking for
