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
import ctrl
from xvfbwrapper import Xvfb
import equipment
import os 

# For normal testing use VIRTUALDISPLAY
# When false, the firefox browser will pop up and display
VIRTUALDISPLAY = True


class T2w(unittest.TestCase):
    def setUp(self):
        p = helpers.findPort()
        server = webctrl.myserver.myserver(host="localhost", port=p)
        server.quiet = True
        print(os.path.dirname(os.path.realpath(__file__)))
        print(os.getcwd())
        e = equipment.allEquipment('src/equipment/*.yaml')
        myequipment = e.get('Grain 3G, 5Gcooler, 5Gpot, platechiller')
    
        controllers = ctrl.setupControllers(False, True, True, myequipment)
        self.brewme = webctrl.runbrew(
            controllers,
            helpers.getTestRecipeList(),
            server)
        self.brewme.startNonBlocking()

        print "up and running"

        if VIRTUALDISPLAY:
            self.vdisplay = Xvfb(width=1280, height=720)
            self.vdisplay.start()

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:%i" % p
        self.verificationErrors = []
        self.accept_next_alert = True

    def url_base(self):
        return(self.base_url)

    def test_recipeliststatus(self):
        print "test_recipeliststatus"
        driver = self.driver
        recipeloadpath = self.url_base() + '/readrecipes'
        print recipeloadpath
        self.driver.get(recipeloadpath)
        print "recipe loaded"
        time.sleep(5)
        self.driver.get(self.url_base())
        print "index page loaded"
        time.sleep(5)
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[4]/button").click()
        self.assertEqual("Recipe list",
                         driver.find_element_by_css_selector("h1").text)
        driver.find_element_by_xpath("(//input[@name='recipe'])[12]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual("17 Falconers Flight IPA",
                         driver.find_element_by_css_selector("form > b").text)
        print "===== SUCCESS test_recipeliststatus ====="

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
        if VIRTUALDISPLAY:
            self.vdisplay.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
