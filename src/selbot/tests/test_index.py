from bottle import app
from selenium import webdriver

from wsgi_liveserver import LiveServerTestCase

# required to load the routes
import main
#import sys
#sys.path.append("../..")
#import bottleweb


class indexTest(LiveServerTestCase):
    def create_app(self):
        return app()

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)
        self.base_url = "http://localhost:8080"

    def tearDown(self):
        self.driver.close()

    def test_index(self):
        self.driver.get(self.base_url + "/")
        self.assertTrue('Hopitty' in self.driver.title)
 
        self.driver.get(self.base_url + "/")
        self.assertTrue('Hopitty' in self.driver.title)

        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("button").click()
        self.assertEqual("Hopitty", driver.find_element_by_css_selector("h1").text)

        driver.get(self.base_url + "/")
        driver.find_element_by_xpath("//a[2]/button").click()
        self.assertEqual("Run Control", driver.find_element_by_css_selector("h1").text)
     
