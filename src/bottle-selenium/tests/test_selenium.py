from bottle import app
from selenium import webdriver
from xvfbwrapper import Xvfb

from wsgi_liveserver import LiveServerTestCase

# required to load the routes
import main
import time


class SeleniumTest(LiveServerTestCase):
    def create_app(self):
        return app()

    def setUp(self):
        self.vdisplay = Xvfb(width=1280, height=720)
        self.vdisplay.start()
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()
        self.vdisplay.stop()

    def test_submit_form(self):
        # Load index page
        self.driver.get(self.url_base())
        self.assertTrue('Useless Query' in self.driver.title)

        # Submit a query
        #field = self.driver.find_element_by_id('query')
        #field.send_keys('something')
        #self.driver.find_element_by_id('submit').click()
        self.driver.find_element_by_id("query").clear()
        self.driver.find_element_by_id("query").send_keys("something")
        self.driver.find_element_by_id("submit").click()

        time.sleep(1)
        # Check the result
        print self.driver.title
        print self.driver.find_element_by_tag_name('body').text
        self.assertTrue('Useless Query Result' in self.driver.title)

        body = self.driver.find_element_by_tag_name('body')
        #self.assertTrue('You searched for "something".' in body.text)
        self.assertTrue('It was useless.' in body.text)
