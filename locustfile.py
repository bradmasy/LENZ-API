import os
from locust import HttpUser, task, events,between
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

# Manually set DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
# # Ensure Django settings are configured
# settings.configure()

# # Function to create a user when the Locust environment is initialized
# @events.init.add_listener
# def on_locust_init(environment, **kwargs):
#     test_user = {
#         "username": "testuser",
#         "email": "testuser@example.com",
#         "first_name": "Test",
#         "last_name": "User",
#         "password": "testpassword",
#     }

#     get_user_model().objects.create_user(
#         email=test_user["email"],
#         username=test_user["username"],
#         first_name=test_user["first_name"],
#         last_name=test_user["last_name"],
#         password=test_user["password"],
#     )

class ListPhotos(HttpUser):
    wait_time = between(1, 3)

    # @task
    def on_start(self):
        # settings.configure()

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
        # self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    @task
    def photo_detail(self):
        headers = {
            "Authorization": "Token " + self.token,
        }
        self.client.get(reverse("photo"), headers=headers)
