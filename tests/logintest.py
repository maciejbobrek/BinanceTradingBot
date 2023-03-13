from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
class ChromeLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver')
    def test_search_in_python_org(self):    
        driver=self.driver
        driver.get("http://127.0.0.1:5000")
        login_bar=driver.find_element("id","email")
        passwod_bar=driver.find_element("id","password")
        login_bar.clear()
        passwod_bar.clear()
        login_bar.send_keys("test@12345.pl")
        passwod_bar.send_keys("test12345")
        passwod_bar.send_keys(Keys.RETURN)
        assert "http://127.0.0.1:5000/" == driver.current_url
    def tearDown(self):
        self.driver.close()
    if __name__ == "__main__":
        unittest.main()