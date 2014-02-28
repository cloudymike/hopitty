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

    def test_recipeselect(self):

        bd = dataMemcache.brewData()
        recipelist = ['coolkoelsh', 'maxhop', 'silverdollar']
        bd.setRecipeList(recipelist)
        bd.setCurrentRecipe('maxhop')
        bd.setSelectedRecipe('maxhop')

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[5]/button").click()
        driver.find_element_by_name("recipe").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual("coolkoelsh", driver.find_element_by_css_selector("form > b").text)
        assert bd.getCurrentRecipe() == 'coolkoelsh'
        assert bd.getSelectedRecipe() == 'coolkoelsh'

        driver.find_element_by_xpath("(//input[@name='recipe'])[3]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual("silverdollar", driver.find_element_by_css_selector("form > b").text)
        assert bd.getCurrentRecipe() == 'silverdollar'
        assert bd.getSelectedRecipe() == 'silverdollar'
