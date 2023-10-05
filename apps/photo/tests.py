from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.photo.serializers import PhotoSerializer
from apps.user.serializers import UserSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.user.models import User


# Create your tests here.
class PhotoTests(TestCase):
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

        user_data = {
            "email": self.test_user.get("email"),
            "password": self.test_user.get("password"),
        }
        response = self.client.post(reverse("login"), user_data, format="json")
        self.token = response.data.get("Token")
        self.user_id = response.data.get("UserId")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_create_photo(self):
        """Test creating a new photo"""
        with open("apps/photo/test_photos/test.png", "rb") as img_file:
            photo_file = SimpleUploadedFile(
                "test.png", img_file.read(), content_type="image/png"
            )

        response = self.client.post(
            reverse("photo-upload"),
            {
                "user_id": self.user_id,
                "photo": photo_file,
                "description": "testdescription",
                "active": True,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("description"), "testdescription")
