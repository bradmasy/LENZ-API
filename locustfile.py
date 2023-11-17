import os
from locust import HttpUser, task, events, between
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.wsgi import get_wsgi_application
import dotenv
import random

# Settings setup for Locust
# to launch locust, use the "locust" command from the main directory in your python virtual env.
# to launch headless use the command "locust --headless --users 10 --spawn-rate 1 -H http://your-server.com"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
dotenv.load_dotenv()
application = get_wsgi_application()

user_number = 0

class ListPhotos(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        user_number = random.randint(0,100000000)
        print(f"starting user {user_number}")
        self.test_user = {
            "username": f"testuser-{user_number}",
            "email": f"testuser-{user_number}@example.com",
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

       # response = self.client.post(reverse("signup"), json=self.test_user)
        #print(response.text)
        response = self.client.post(reverse("login"), user_data)
        response_data = response.json()
        self.token = response_data.get("Token")
        self.user_id = response_data.get("UserId")
        user_number += 1
        # self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    @task
    def photo_endpoint(self):
        headers = {
            "Authorization": "Token " + self.token,
        }
        response = self.client.get(reverse("photo") , headers=headers).json()
        print(response)
