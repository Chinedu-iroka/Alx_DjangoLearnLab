from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'books_all', views.BookViewSet, basename='book_all')

# Define the app name for namespacing (optional but recommended)
app_name = 'api'

urlpatterns = [
    # Main endpoint for listing books
    path('books/', views.BookList.as_view(), name='book-list'),
    
    # Alternative endpoint that supports both listing and creating books
    # Uncomment the line below if you want to use BookListCreate instead
    # path('books/', views.BookListCreate.as_view(), name='book-list-create'),
    path('', include(router.urls)),
]