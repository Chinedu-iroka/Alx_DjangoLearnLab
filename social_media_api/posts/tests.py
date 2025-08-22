from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class FeedAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        
        # Create posts from user2
        self.post1 = Post.objects.create(
            author=self.user2,
            title='Post 1',
            content='Content 1'
        )
        self.post2 = Post.objects.create(
            author=self.user2,
            title='Post 2',
            content='Content 2'
        )

    def test_feed_without_following(self):
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_feed_with_following(self):
        # Follow user2
        self.user1.follow(self.user2)
        
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)