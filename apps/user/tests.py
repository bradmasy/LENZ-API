from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User  # Import your User model
from django.db.models import Q
from django.contrib.auth import get_user_model



class UsersViewTest(TestCase):
    # This will be used to store the user created in setUp
    def setUp(self):
        self.client = APIClient()
        self.test_user = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword",
        }

        get_user_model().objects.create_user(
            email=self.test_user.get("email"),
            username=self.test_user.get("username"),
            first_name=self.test_user.get("first_name"),
            last_name=self.test_user.get("last_name"),
            password=self.test_user.get("password"),
        )

    def test_create_user(self):
        """Test creating a new user"""

        user_data = {
            "username": "testuser1",
            "email": "testuser1@example.com",
            "first_name": "Test1",
            "last_name": "User1",
            "password": "testpassword1",
        }
        response = self.client.post(reverse("signup"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(Q(username=user_data["username"]))
        self.assertEqual(user.username, user_data["username"])
        self.assertEqual(user.email, user_data["email"])
        self.assertEqual(user.first_name, user_data["first_name"])
        self.assertEqual(user.last_name, user_data["last_name"])

    def test_log_user_in(self):
        """Test logging in an already existing user."""
        email = self.test_user.get("email")
        password = self.test_user.get("password")
        user_data = {"email": email, "password": password}
        response = self.client.post(reverse("login"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Token", response.data)
        self.assertIn("UserId", response.data)
