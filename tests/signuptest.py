from selenium import webdriver
import random
import string
from selenium.webdriver.common.keys import Keys
import unittest
class ChromeSignup(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver')
    def test_search_in_python_org(self):    
        driver=self.driver
        driver.get("http://127.0.0.1:5000/signup")
        email_bar=driver.find_element("id","email")
        passwod1_bar=driver.find_element("id","password1")
        passwod2_bar=driver.find_element("id","password2")
        firstName_bar=driver.find_element("id","firstName")
        randomstring=''.join(random.choices(string.ascii_lowercase, k=5))
        email_bar.clear()
        passwod1_bar.clear()
        passwod2_bar.clear()
        firstName_bar.clear()
        email_bar.send_keys(randomstring+"@12.pl")
        firstName_bar.send_keys("name")
        passwod1_bar.send_keys("test12345")
        passwod2_bar.send_keys("test12345")
        passwod2_bar.send_keys(Keys.RETURN)
        assert "http://127.0.0.1:5000/" == driver.current_url
    def tearDown(self):
        self.driver.close()
    if __name__ == "__main__":
        unittest.main()