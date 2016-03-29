import unittest
import os
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


class GeneralTest(unittest.TestCase):



    def setUp(self):
        # chromedriver = "/usr/local/bin/chromedriver"
        # os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Firefox()

    def testSuccessfullLogin(self):
        driver = self.driver
        driver.get("http://localhost:8000/")
        login = driver.find_element_by_css_selector("a[href='/accounts/login/']")
        login.click()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").send_keys("admin")
        # Click on Sign in button
        driver.find_element_by_css_selector(".btn-primary").click()

        # Check the presence of main dashboards sections
        self.assertIsNotNone(driver.find_element_by_xpath("//h3[text()='My projects']"),
                             "The 'My projects' section is not displayed")
        self.assertIsNotNone(driver.find_element_by_xpath("//h3[text()=' Issues assigned to me']"),
                             "The 'Issues assigned to me' section is not displayed")
        self.assertIsNotNone(driver.find_element_by_xpath("//h3[text()=' Issues created by me']"),
                             "The 'Issues created by me' section is not displayed")

    def testLoginWihtInvalidPassword(self):
        driver = self.driver
        driver.get("http://localhost:8000/")
        login = driver.find_element_by_css_selector("a[href='/accounts/login/']")
        login.click()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").send_keys("admin-invalid")
        # Click on Sign in button
        driver.find_element_by_css_selector(".btn-primary").click()

        # Verify if the warning message is displayed and the content of the warning message
        self.assertIsNotNone(driver.find_element_by_css_selector(".alert"), "There is no warning message present.")
        print(driver.find_element_by_css_selector(".alert").text)
        self.assertTrue("Please enter a correct username and password. Note that both fields may be case-sensitive." in
                        driver.find_element_by_css_selector(".alert").text,
                        "The warning message is not the expected one.")

    def testLoginWihtInvalidUsername(self):
        driver = self.driver
        driver.get("http://localhost:8000/")
        login = driver.find_element_by_css_selector("a[href='/accounts/login/']")
        login.click()
        driver.find_element_by_id("id_username").send_keys("admin-invalid")
        driver.find_element_by_id("id_password").send_keys("admin")
        # Click on Sign in button
        driver.find_element_by_css_selector(".btn-primary").click()

        # Verify if the warning message is displayed and the content of the warning message
        self.assertIsNotNone(driver.find_element_by_css_selector(".alert"), "There is no warning message present.")
        print(driver.find_element_by_css_selector(".alert").text)
        self.assertTrue("Please enter a correct username and password. Note that both fields may be case-sensitive." in
                        driver.find_element_by_css_selector(".alert").text,
                        "The warning message is not the expected one.")

    def testLoginWihtInvalidUsernameAndInvalidPassword(self):
        driver = self.driver
        driver.get("http://localhost:8000/")
        login = driver.find_element_by_css_selector("a[href='/accounts/login/']")
        login.click()
        driver.find_element_by_id("id_username").send_keys("admin-invalid")
        driver.find_element_by_id("id_password").send_keys("admin-invalid")
        # Click on Sign in button
        driver.find_element_by_css_selector(".btn-primary").click()

        # Verify if the warning message is displayed and the content of the warning message
        self.assertIsNotNone(driver.find_element_by_css_selector(".alert"), "There is no warning message present.")
        print(driver.find_element_by_css_selector(".alert").text)
        self.assertTrue("Please enter a correct username and password. Note that both fields may be case-sensitive." in
                        driver.find_element_by_css_selector(".alert").text,
                        "The warning message is not the expected one.")

    def tearDown(self):
        self.driver.close();

    if __name__ == "__main__":
        unittest.main()