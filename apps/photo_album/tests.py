from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


class PhotoAlbumTests(TestCase):
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

    def test_create_photo_album(self):
        """Test creating a new photo album"""

        response = self.client.post(
            reverse("photo-album-create"),
            {
                "user_id": self.user_id,
                "title": "testtitle",
                "description": "testdescription",
                "active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("title"), "testtitle")

    def test_get_photo_album(self):
        """Test getting a photo album"""

        response = self.client.post(
            reverse("photo-album-create"),
            {
                "user_id": self.user_id,
                "title": "testtitle",
                "description": "testdescription",
                "active": True,
            },
            format="json",
        )

        response = self.client.get(reverse("photo-album-list"))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(response.data.get("results")[0].get("title"), "testtitle")
