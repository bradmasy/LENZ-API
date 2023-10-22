from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

api_url = "https://lenz-5f9c8ee2c363.herokuapp.com/"


class HostTest(LiveServerTestCase):
    # def setUpClass(cls):
    #     super().setUpClass()

    @classmethod 
    def setUpClass(cls):
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)
        super().setUpClass()
        
    
    @classmethod
    def tearDownClass(cls):
        # cls.selenium.quit()
        super().tearDownClass()
        
    def test_api_root(self):

        print("Current URL:", self.selenium.current_url)  # Add this line for debugging

        self.selenium.get(f"{api_url}")
        assert "Api Root – Django REST framework" in self.selenium.title
        
