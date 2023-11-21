from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from urllib.parse import urlencode


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
        with open("apps/photo/test_photos/test.jpg", "rb") as img_file:
            photo_file = SimpleUploadedFile(
                "test.jpg", img_file.read(), content_type="image/jpg"
            )
        response = self.client.post(
            reverse("photo"),
            {
                "user_id": self.user_id,
                "title": "my title",
                "photo": photo_file,
                "description": "test description",
                "active": True,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data.get("photo").get("description"), "test description"
        )

    def test_create_photo_no_user_id(self):
        with open("apps/photo/test_photos/test.jpg", "rb") as img_file:
            photo_file = SimpleUploadedFile(
                "test.jpg", img_file.read(), content_type="image/jpg"
            )
        response = self.client.post(
            reverse("photo"),
            {
                "title": "my title",
                "photo": photo_file,
                "description": "test description",
                "active": True,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)

    def test_create_photo_no_title(self):
        with open("apps/photo/test_photos/test.jpg", "rb") as img_file:
            photo_file = SimpleUploadedFile(
                "test.jpg", img_file.read(), content_type="image/jpg"
            )

        response = self.client.post(
            reverse("photo"),
            {
                "user_id": self.user_id,
                "photo": photo_file,
                "description": "test description",
                "active": True,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)

    def test_create_photo_no_photo(self):
        response = self.client.post(
            reverse("photo"),
            {
                "user_id": self.user_id,
                "title": "my title",
                "description": "test description",
                "active": True,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)

    def test_get_photo(self):
        """Test getting a photo"""
        with open("apps/photo/test_photos/test.jpg", "rb") as img_file:
            photo_file = SimpleUploadedFile(
                "test.jpg", img_file.read(), content_type="image/jpg"
            )

        self.client.post(
            reverse("photo"),
            {
                "user_id": self.user_id,
                "title": "my title",
                "photo": photo_file,
                "description": "test description",
                "active": True,
            },
            format="multipart",
        )

        url = reverse("photo")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(
            response.data.get("results")[0].get("description"), "test description"
        )

    def test_delete_photo(self):
        with open("apps/photo/test_photos/test.jpg", "rb") as img_file:
            photo_file = SimpleUploadedFile(
                "test.jpg", img_file.read(), content_type="image/jpg"
            )

        response = self.client.post(
            reverse("photo"),
            {
                "user_id": self.user_id,
                "title": "my title",
                "photo": photo_file,
                "description": "test description",
                "active": True,
            },
            format="multipart",
        )

        id = response.data.get("photo").get("id")
        response = self.client.delete(reverse("photo-by-id", args=[id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.get("message"), "Photo Album Successfully Deleted"
        )

        response = self.client.get(reverse("photo"))

        self.assertEqual(len(response.data.get("results")), 0)

        response = self.client.get(reverse("photo-by-id", args=[id]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get("error"), "Photo matching query does not exist."
        )

    def test_search_photos(self):
        titles = ["my title", "this title", "daily photo", "random"]
        descriptions = ["mountain", "sunny day", "fun", "great day"]

        for i in range(0, len(titles)):
            title = titles[i]

            for j in range(0, len(descriptions)):
                description = descriptions[j]

                for k in range(0, 5):
                    with open("apps/photo/test_photos/test.jpg", "rb") as img_file:
                        photo_file = SimpleUploadedFile(
                            "test.jpg", img_file.read(), content_type="image/jpg"
                        )
                    self.client.post(
                        reverse("photo"),
                        {
                            "user_id": self.user_id,
                            "title": title,
                            "photo": photo_file,
                            "description": description,
                            "active": True,
                        },
                        format="multipart",
                    )

        query = {"title": "my title"}

        response = self.client.get(reverse("photo") + "?" + urlencode(query))
        self.assertEqual(response.data.get("count"), 20)

        query = {"title": "my title", "description": "mountain"}

        response = self.client.get(reverse("photo") + "?" + urlencode(query))
        self.assertEqual(response.data.get("count"), 5)

        to_date_str = "2023-12-31"
        from_date_str = "2023-09-01"
        query = {"to_date": to_date_str, "from_date": from_date_str}
        response = self.client.get(reverse("photo") + "?" + urlencode(query))
        self.assertEqual(response.data.get("count"), 80)

    def test_tag_photos(self):
        with open("apps/photo/test_photos/test.jpg", "rb") as img_file:
            photo_file = SimpleUploadedFile(
                "test.jpg", img_file.read(), content_type="image/jpg"
            )
        response = self.client.post(
            reverse("photo"),
            {
                "user_id": self.user_id,
                "title": "my title",
                "photo": photo_file,
                "description": "test description",
                "active": True,
            },
            format="multipart",
        )

        photo_id = response.data.get("photo")["id"]

        tag_name = "awesome"
        response = self.client.post(
            reverse("tag"), {"name": tag_name, "photo_id": photo_id}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("data").get("Tag"), "awesome")
        self.assertEqual(int(response.data.get("data").get("Photo")), int(photo_id))


# Photo Album Photo Tests


class PhotoAlbumPhotoTests(TestCase):
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

        response = self.client.post(
            reverse("photo-album"),
            {
                "user_id": self.user_id,
                "title": "testtitle",
                "description": "testdescription",
                "active": True,
            },
            format="json",
        )
        self.album = response.data.get("photo_album", None)

        with open("apps/photo/test_photos/test.jpg", "rb") as img_file:
            photo_file = SimpleUploadedFile(
                "test.jpg", img_file.read(), content_type="image/jpg"
            )

        response = self.client.post(
            reverse("photo"),
            {
                "user_id": self.user_id,
                "title": "my photo",
                "photo": photo_file,
                "description": "testdescription",
                "active": True,
                "title": "my photo",
            },
            format="multipart",
        )
        self.photo = response.data.get("photo", None)

    def test_create_photo_album_photo(self):
        payload = {
            "photo_id": self.photo.get("id"),
            "photo_album_id": self.album.get("id"),
        }

        response = self.client.post(
            reverse("photo-album-photo"),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data.get("photo_album_photo").get("photo_id"), self.photo.get("id")
        )
        self.assertEqual(
            response.data.get("photo_album_photo").get("photo_album_id"),
            self.album.get("id"),
        )

    def test_get_photo_album_photo(self):
        payload = {
            "photo_id": self.photo.get("id"),
            "photo_album_id": self.album.get("id"),
        }

        self.client.post(reverse("photo-album-photo"), payload, format="json")

        url = reverse("photo-album-photo")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(
            response.data.get("results")[0].get("photo_id"), self.photo.get("id")
        )
        self.assertEqual(
            response.data.get("results")[0].get("photo_album_id"), self.album.get("id")
        )
