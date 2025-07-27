from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .forms import SearchForm
from .models import Book
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    # TODO: Add form handling logic here
    return render(request, 'bookshelf/book_form.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # TODO: Add form handling logic here
    return render(request, 'bookshelf/book_form.html', {'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')

def book_search(request):
    results = []
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['title']
            results = Book.objects.filter(title__icontains=query)
    else:
        form = SearchForm()
    return render(request, 'bookshelf/book_search.html', {'form': form, 'results': results})