from book.models import Book

# Update the title
b = Book.objects.get(title="1984")
b.title = "Nineteen Eighty-Four"
b.save()
print(b.title)
# Output: Nineteen Eighty-Four