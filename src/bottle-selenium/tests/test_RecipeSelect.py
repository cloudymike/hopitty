from bottle import app
from selenium import webdriver

from my_wsgi_liveserver import LiveServerTestCase
from xvfbwrapper import Xvfb

# required to load the routes
import hopmain
import dataMemcache


class hopTestRecipeSelect(LiveServerTestCase):
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
        bd.setSelectedRecipe('maxhop')

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[5]/button").click()
        driver.find_element_by_name("recipe").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual("coolkoelsh",
                         driver.find_element_by_css_selector("form > b").text)
        assert bd.getSelectedRecipe() == 'coolkoelsh'

        driver.find_element_by_xpath("(//input[@name='recipe'])[3]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual("silverdollar",
                         driver.find_element_by_css_selector("form > b").text)
        assert bd.getSelectedRecipe() == 'silverdollar'

    def test_currentRecipe(self):

        bd = dataMemcache.brewData()
        recipelist = ['coolkoelsh', 'maxhop', 'silverdollar']
        bd.setRecipeList(recipelist)
        bd.setSelectedRecipe('maxhop')
        bd.setCurrentRecipe('maxhop')
        bd.setCurrentStage('First')
        bd.setControllersStatus({})
        bd.resetWatchdog()
        bd.setCtrlRunning(True)
        bd.setPause(False)

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        # Go to status page and check recipe
        driver.find_element_by_xpath("//a[3]/button").click()
        self.assertEqual("Brew Status",
                         driver.find_element_by_css_selector("h1").text)
        self.assertEqual("maxhop",
                         driver.find_element_by_css_selector("h2").text)

        # Go to reciple list page and set recipe
        driver.find_element_by_xpath("//a[5]/button").click()
        driver.find_element_by_name("recipe").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual("coolkoelsh",
                         driver.find_element_by_css_selector("form > b").text)
        assert bd.getSelectedRecipe() == 'coolkoelsh'

        driver.find_element_by_xpath("(//input[@name='recipe'])[3]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual("silverdollar",
                         driver.find_element_by_css_selector("form > b").text)
        assert bd.getSelectedRecipe() == 'silverdollar'

        # Go back to status page.
        #Current recipe is still the same, controller needs to stop
        driver.find_element_by_xpath("//a[3]/button").click()
        self.assertEqual("Brew Status",
                         driver.find_element_by_css_selector("h1").text)
        self.assertEqual("maxhop",
                         driver.find_element_by_css_selector("h2").text)

        # Simulate a start top to get selected recipe to current recipe
        recipe = bd.getSelectedRecipe()
        bd.setCurrentRecipe(recipe)

        # Reload status page.
        # Current recipe is still the same, controller needs to stop
        driver.find_element_by_xpath("//a[3]/button").click()
        self.assertEqual("Brew Status",
                         driver.find_element_by_css_selector("h1").text)
        self.assertEqual("silverdollar",
                         driver.find_element_by_css_selector("h2").text)
