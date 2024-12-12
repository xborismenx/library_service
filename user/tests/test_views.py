from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

ME_URL = reverse("user:me")
CREATE_USER_URL = reverse("user:create-user")


class UserCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "email": "testuser@example.com",
            "password": "strongpassword123",
        }
        self.invalid_payload = {
            "email": "",
            "password": "",
        }

    def test_create_user_with_valid_payload(self):
        response = self.client.post(CREATE_USER_URL, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.valid_payload["email"]).exists())

    def test_create_user_with_invalid_payload(self):
        response = self.client.post(CREATE_USER_URL, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MeApiViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="user@example.com", password="password123")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {self.token}")

    def test_get_current_user_profile(self):
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_current_user_profile(self):
        updated_data = {"email": "updateduser@example.com"}
        response = self.client.patch(ME_URL, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, updated_data["email"])
