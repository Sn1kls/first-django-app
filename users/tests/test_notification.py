from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Notification


class UserNotificationsAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@example.com", password="password123")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password123")

        for _ in range(15):
            Notification.objects.create(user=self.user1, content=f"Notifcation for {_+1} for user1")

        for _ in range(5):
            Notification.objects.create(user=self.user2, content=f"Notifcation for {_+1} for user2")

        self.user1_token = self.client.post(
            reverse("token_obtain_pair"), {"email": "user1@example.com", "password": "password123"}
        ).data["access"]

        self.user2_token = self.client.post(
            reverse("token_obtain_pair"), {"email": "user2@example.com", "password": "password123"}
        ).data["access"]

        self.notification_url = reverse("user_notifications")

    def test_authentication_required(self):
        response = self.client.get(self.notification_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_user_notifications(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user1_token}")
        response = self.client.get(self.notification_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

        self.assertEqual(response.data["count"], 15)

        results = response.data["results"]
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0]["content"], "Notifcation for 15 for user1")
