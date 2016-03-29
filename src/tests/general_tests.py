import unittest
import os
from selenium import webdriver

class GeneralTest(unittest.TestCase):



    def setUp(self):
        # chromedriver = "/usr/local/bin/chromedriver"
        # os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Firefox()

    def test1(self):
        driver = self.driver;
        driver.get("http://localhost:8000")
        login = driver.find_element_by_css_selector("a[href='/accounts/login/']")
        login.click()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").send_keys("admin")
        driver.find_element_by_css_selector(".btn-primary").click()


    def tearDown(self):
        self.driver.close();

    if __name__ == "__main__":
        unittest.main()