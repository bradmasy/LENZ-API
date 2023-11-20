import dotenv
import os
import random
import time
from locust import HttpUser, task, events, between
from locust.runners import MasterRunner
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.wsgi import get_wsgi_application

# Settings setup for Locust
# to launch locust, use the "locust" command from the main directory in your python virtual env.
# to launch headless use the command "locust --headless --users 10 --spawn-rate 1 -H http://your-server.com"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
dotenv.load_dotenv()
application = get_wsgi_application()


class ListPhotos(HttpUser):
    wait_time = between(3, 5)
    user_data_ready = False
    photo_completed = False
    test_completion = False

    def on_locust_init(self, **kwargs):
        if isinstance(self.environment.runner, MasterRunner):
            print("I'm on master node")
        else:
            print("I'm on a worker or standalone node")

    def check_test_completion(self):
        if self.user_data_ready and self.photo_completed:
            self.test_completion = True

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        print("A new test is starting")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        print("A new test is ending")

    def wait_for_user_data(self):
        while not self.user_data_ready:
            time.sleep(2)

    def on_start(self):
        self.user_number = random.randint(0, 100000000)
        print(f"starting user {self.user_number}")

        self.test_user = {
            "username": f"testuser-{self.user_number}",
            "email": f"testuser-{self.user_number}@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword",
        }

        # get_user_model().objects.create_user(
        #     email=self.test_user.get("email"),
        #     username=self.test_user.get("username"),
        #     first_name=self.test_user.get("first_name"),
        #     last_name=self.test_user.get("last_name"),
        #     password=self.test_user.get("password"),
        # )

        user_data = {
            "email": self.test_user.get("email"),
            "password": self.test_user.get("password"),
        }

        self.client.post(reverse("signup"), json=self.test_user)

        response = self.client.post(reverse("login"), user_data)
        response_data = response.json()
        self.token = response_data.get("Token")
        self.user_id = response_data.get("UserId")
        self.user_data_ready = True

    def on_stop(self):
        print(f"Stopping now with user: {self.user_number}")

        headers = {
            "Authorization": "Token " + self.token,
        }
        self.client.delete(
            reverse("user-delete", kwargs={"pk": self.user_id}), headers=headers
        )

    @task
    def photo_endpoint(self):
        print("get photo load test")

        headers = {
            "Authorization": "Token " + self.token,
        }

        with self.client.get(
            reverse("photo"), headers=headers, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()

        self.photo_completed = True
