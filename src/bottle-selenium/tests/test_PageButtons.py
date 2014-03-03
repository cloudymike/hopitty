from bottle import app
from selenium import webdriver

from wsgi_liveserver import LiveServerTestCase
from xvfbwrapper import Xvfb

# required to load the routes
import hopmain
import dataMemcache


class hopTestPageButtons(LiveServerTestCase):
    def create_app(self):
        return app()

    def setUp(self):
        self.vdisplay = Xvfb(width=1280, height=720)
        self.vdisplay.start()
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()
        self.vdisplay.stop()

    def test_index(self):

        driver = self.driver
        self.driver.get(self.url_base())
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_css_selector("button").click()
        self.assertEqual("Hopitty",
                         driver.find_element_by_css_selector("h1").text)

    def test_RunControl(self):

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[2]/button").click()
        self.assertEqual("Run Control",
                         driver.find_element_by_css_selector("h1").text)

    def test_status(self):

        bd = dataMemcache.brewData()
        recipelist = ['coolkoelsh', 'maxhop', 'silverdollar']
        bd.setRecipeList(recipelist)
        bd.setSelectedRecipe('silverdollar')

        bd.setCurrentRecipe('silverdollar')
        bd.setCurrentStage('First')
        bd.setControllersStatus({})
        bd.resetWatchdog()
        bd.setCtrlRunning(True)
        bd.setPause(False)

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[3]/button").click()
        self.assertEqual("Brew Status",
                         driver.find_element_by_css_selector("h1").text)

    def test_stages(self):

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[4]/button").click()
        self.assertEqual("Brew Stages",
                         driver.find_element_by_css_selector("h1").text)
        driver.find_element_by_css_selector("button").click()
        self.assertEqual("Hopitty",
                         driver.find_element_by_css_selector("h1").text)

    def test_recipelist(self):

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[5]/button").click()
        self.assertEqual("Recipe list",
                         driver.find_element_by_css_selector("h1").text)
        driver.find_element_by_css_selector("button").click()
        self.assertEqual("Hopitty",
                         driver.find_element_by_css_selector("h1").text)

    def test_recipe(self):

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[6]/button").click()
        self.assertEqual("Recipe",
                         driver.find_element_by_css_selector("h1").text)
        driver.find_element_by_css_selector("button").click()
        self.assertEqual("Hopitty",
                         driver.find_element_by_css_selector("h1").text)
