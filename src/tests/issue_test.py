import random
import unittest
from selenium import webdriver

class IssueTests(unittest.TestCase):

    def setUp(self):
        # chromedriver = "/usr/local/bin/chromedriver"
        # os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Firefox()

    def testAddIssue(self):

        rand = random.randint(1, 1000);
        driver = self.driver
        driver.get("http://localhost:8000/")
        login = driver.find_element_by_css_selector("a[href='/accounts/login/']")
        login.click()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").send_keys("admin")
        # Click on Sign in button
        driver.find_element_by_css_selector(".btn-primary").click()

		driver.find_element_by_css_selector("a[href='/uks/project_view/1']").click()
		driver.find_element_by_xpath("//a[text()='New issue']").click()

		driver.find_element_by_id("id_tittle").send_keys("issue" + str(rand))
		driver.find_element_by_id("id_date").send_keys("2011-01-01")
		driver.find_element_by_id("id_project").send_keys("pr" + str(rand))
		driver.find_element_by_id("id_reporter").send_keys("admin")

		driver.find_element_by_css_selector(".dropdown-toggle").click()
        driver.find_element_by_xpath("//option[text()='admin']").click()

		driver.find_element_by_css_selector(".dropdown-toggle").click()
        driver.find_element_by_xpath("//option[text()='done']").click()

		driver.find_element_by_css_selector(".dropdown-toggle").click()
        driver.find_element_by_xpath("//option[text()='deploy']").click()

		driver.find_element_by_css_selector(".dropdown-toggle").click()
        driver.find_element_by_xpath("//option[text()='bug']").click()

		driver.find_element_by_css_selector(".dropdown-toggle").click()
        driver.find_element_by_xpath("//option[text()='minor']").click()

        driver.find_element_by_css_selector("button[type='submit']").click()



    def tearDown(self):
        self.driver.close()

    if __name__ == "__main__":
        unittest.main()