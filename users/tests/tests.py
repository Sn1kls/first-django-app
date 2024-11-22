from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, UserRoles


class TestUserViews(APITestCase):
    def setUp(self):
        self.adminUser = User.objects.create_user(email="mkasw123@gmail.com", password="admin123", role=UserRoles.ADMIN)
        self.managerUser = User.objects.create_user(
            email="manager1@gmail.com", password="manager123", role=UserRoles.MANAGER
        )
        self.user = User.objects.create_user(email="user1@gmail.com", password="user123", role=UserRoles.DEFAULT_USER)

        self.url = reverse("user_list")

    def test_admin_can_view_all_users(self):
        self.client.force_authenticate(user=self.adminUser)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("results", response.data)
        user_data = response.data["results"]

        self.assertGreaterEqual(len(user_data), 3)
        self.assertTrue(any(user["email"] == "mkasw123@gmail.com" for user in user_data))

    def test_manager_can_view_all_users(self):
        self.client.force_authenticate(user=self.managerUser)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("results", response.data)
        user_data = response.data["results"]

        self.assertGreaterEqual(len(user_data), 3)

    def test_user_cannot_view_all_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_view_all_users(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        User.objects.all().delete()
