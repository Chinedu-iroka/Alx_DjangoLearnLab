from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowAPITestCase(APITestCase):
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

    def test_follow_user(self):
        response = self.client.post('/api/auth/follow/', {'user_id': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1.is_following(self.user2))

    def test_unfollow_user(self):
        self.user1.follow(self.user2)
        response = self.client.post('/api/auth/unfollow/', {'user_id': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user1.is_following(self.user2))

    def test_cannot_follow_self(self):
        response = self.client.post('/api/auth/follow/', {'user_id': self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)