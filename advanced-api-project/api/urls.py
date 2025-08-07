from django.urls import path
from .views import AuthorListView
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateCustomView,
    BookDeleteCustomView,
)

urlpatterns = [
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/', BookUpdateCustomView.as_view(), name='book-update'),
    path('books/delete/', BookDeleteCustomView.as_view(), name='book-delete'),
]