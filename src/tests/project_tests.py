import random
import unittest
from selenium import webdriver

class ProjectTests(unittest.TestCase):

    def setUp(self):
        # chromedriver = "/usr/local/bin/chromedriver"
        # os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Firefox()

    def testAddNewProject(self):
        driver = self.driver
        driver.get("http://localhost:8000/")
        login = driver.find_element_by_css_selector("a[href='/accounts/login/']")
        login.click()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").send_keys("admin")
        # Click on Sign in button
        driver.find_element_by_css_selector(".btn-primary").click()

        # Click on dropdown
        driver.find_element_by_css_selector(".dropdown-toggle").click()
        driver.find_element_by_xpath("//a[text()='New Project']").click()

        rand = random.randint(1, 1000);
        driver.find_element_by_id("id_name").send_keys("project" + str(rand))
        driver.find_element_by_id("id_key").send_keys("pr" + str(rand))
        driver.find_element_by_id("id_git").send_keys("https://github.com/ftn-tim2/jsd-project.git")
        driver.find_element_by_xpath("//option[text()='admin']").click()
        driver.find_element_by_id("id_description").send_keys("Some descriptions.")

        # Click on the save button
        driver.find_element_by_css_selector("button[type='submit']").click()

        # # Check the presence of main dashboards sections
        # self.assertIsNotNone(driver.find_element_by_xpath("//h3[text()='My projects']"),
        #                      "The 'My projects' section is not displayed")
        # self.assertIsNotNone(driver.find_element_by_xpath("//h3[text()=' Issues assigned to me']"),
        #                      "The 'Issues assigned to me' section is not displayed")
        # self.assertIsNotNone(driver.find_element_by_xpath("//h3[text()=' Issues created by me']"),
        #                      "The 'Issues created by me' section is not displayed")

    def tearDown(self):
        self.driver.close()

    if __name__ == "__main__":
        unittest.main()