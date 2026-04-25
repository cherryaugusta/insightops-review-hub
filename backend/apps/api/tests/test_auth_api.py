from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthApiTests(APITestCase):
    def test_register_creates_user(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "demo1",
                "email": "demo1@example.com",
                "first_name": "Demo",
                "last_name": "One",
                "password": "StrongPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="demo1").exists())

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            username="existing",
            email="existing@example.com",
            password="StrongPassword123!",
        )
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "newuser",
                "email": "existing@example.com",
                "first_name": "Demo",
                "last_name": "Two",
                "password": "StrongPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_obtain_works(self):
        User.objects.create_user(
            username="demoanalyst",
            email="demoanalyst@example.com",
            password="StrongPassword123!",
        )
        response = self.client.post(
            "/api/token/",
            {"username": "demoanalyst", "password": "StrongPassword123!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_me_requires_auth(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_current_user_only(self):
        user = User.objects.create_user(
            username="demoanalyst",
            email="demoanalyst@example.com",
            password="StrongPassword123!",
            first_name="Demo",
            last_name="Analyst",
        )
        token_response = self.client.post(
            "/api/token/",
            {"username": "demoanalyst", "password": "StrongPassword123!"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "demoanalyst")
        self.assertEqual(response.data["email"], user.email)
