from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    def test_display_name_falls_back_to_username(self):
        user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="StrongPassword123!",
        )
        self.assertEqual(user.display_name, "tester")

    def test_display_name_uses_full_name(self):
        user = User.objects.create_user(
            username="tester2",
            email="tester2@example.com",
            password="StrongPassword123!",
            first_name="Demo",
            last_name="Analyst",
        )
        self.assertEqual(user.display_name, "Demo Analyst")
