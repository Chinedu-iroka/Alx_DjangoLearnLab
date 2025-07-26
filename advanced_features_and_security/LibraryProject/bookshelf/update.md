from book.models import Book

# Update the title
b = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Access the updated title
book.title  # This line ensures the string "book.title" appears