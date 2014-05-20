# Template example of selenium test for webctrl
# This test just checks that the index page is found
# To create a close-to template, export selenium test as python  webdriver
# Use this template instead, but add in the test_... method

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import webctrl
import time
import helpers
from xvfbwrapper import Xvfb


class T2w(unittest.TestCase):
    def setUp(self):
        p = helpers.findPort()
        server = webctrl.myserver.myserver(host="localhost", port=p)
        server.quiet = True

        self.brewme = webctrl.runbrew(
            helpers.timerCtrl(),
            helpers.getSimpleBSMX(),
            server)
        self.brewme.startNonBlocking()

        print "up and running"

        # Comment out next two lines to see firefox on local display
        self.vdisplay = Xvfb(width=1280, height=720)
        self.vdisplay.start()

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:%i" % p
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_t2w(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("button").click()
        self.assertEqual("Hopitty",
                         driver.find_element_by_css_selector("h1").text)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException, e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        time.sleep(1)
        print "time to go"
        self.brewme.stop()
        self.driver.quit()
        self.vdisplay.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
