from bottle import app
from selenium import webdriver

from wsgi_liveserver import LiveServerTestCase

# required to load the routes
import hopmain


class hopTestPageButtons(LiveServerTestCase):
    def create_app(self):
        return app()

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_index(self):

        driver = self.driver
        self.driver.get(self.url_base())
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_css_selector("button").click()
        self.assertEqual("Hopitty", driver.find_element_by_css_selector("h1").text)

    def test_RunControl(self):

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[2]/button").click()
        self.assertEqual("Run Control", driver.find_element_by_css_selector("h1").text)

