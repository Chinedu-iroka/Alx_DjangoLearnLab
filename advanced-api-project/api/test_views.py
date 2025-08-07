from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')

        # Login client
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # Create sample book
        self.book = Book.objects.create(title="Test Book", author="Author A", description="Some description")

    def test_create_book(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Book",
            "author": "Author B",
            "description": "A new book for testing"
        }
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "description": "Updated Description"
        }
        response = self.client.put(reverse('book-detail', args=[self.book.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        self.client.force_authenticate(user=self.admin_user)  # Make sure only admin can delete
        response = self.client.delete(reverse('book-detail', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_author(self):
        Book.objects.create(title="Another Book", author="Author A", description="Another one")
        response = self.client.get(reverse('book-list') + '?author=Author A')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_books(self):
        response = self.client.get(reverse('book-list') + '?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.post(reverse('book-list'), {"title": "No Auth", "author": "X", "description": "Y"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    """
Testing Approach (Documentation)

- Tool: Django `unittest` via `APITestCase`
- Covered: CRUD operations, filtering, search, authentication
- Execution: Run tests with `python manage.py test api`
- Expected Outcome: All tests should pass; verify API correctness and permission handling
"""