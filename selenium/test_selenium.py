from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

api_url = "https://lenz-5f9c8ee2c363.herokuapp.com/"


class HostTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        cls.selenium = webdriver.Chrome(options=chrome_options)
        cls.selenium.implicitly_wait(10)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_api_root(self):
        print("Current URL:", self.selenium.current_url)  # Add this line for debugging

        self.selenium.get(f"{api_url}")
        assert "Api Root – Django REST framework" in self.selenium.title
