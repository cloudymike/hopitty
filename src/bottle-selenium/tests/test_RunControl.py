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

    def test_StartStop(self):

        bd = dataMemcache.brewData()
        recipelist = ['coolkoelsh', 'maxhop', 'silverdollar']
        bd.setRecipeList(recipelist)
        bd.setCurrentRecipe('silverdollar')
        bd.setSelectedRecipe('silverdollar')
        status = {}
        status['name'] = 'silverdollar'
        status['stage'] = 'First'
        bd.setStatus(status)
        bd.setRunStatus('stop')
        bd.setPause(False)

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[2]/button").click()
        self.assertEqual(
            'Run Control\nCurrent Recipe: silverdollar\n' +
            'Current Stage:\nRun status: Stopped\nStart/stop ' +
            'brewing program\nPause brewing process temporarily\nSkip one ' +
            'stage forward.\nClear error.\n\n\nHomeRun ' +
            'ControlStatusStagesRecipeListRecipe',
            driver.find_element_by_css_selector("body").text)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual(
            'Run Control\nCurrent Recipe: silverdollar\nCurrent Stage: First\nRun status: ' +
            'Running\nStart/stop brewing program\nPause brewing process ' +
            'temporarily\nSkip one stage forward.\nClear error.\n\n\n' +
            'HomeRun ControlStatusStagesRecipeListRecipe',
            driver.find_element_by_css_selector("body").text)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual(
            'Run Control\nCurrent Recipe: silverdollar\n' +
            'Current Stage:\nRun status: Stopped\nStart/stop ' +
            'brewing program\nPause brewing process temporarily\nSkip one ' +
            'stage forward.\nClear error.\n\n\nHomeRun ' +
            'ControlStatusStagesRecipeListRecipe',
            driver.find_element_by_css_selector("body").text)

    def test_Pause(self):

        bd = dataMemcache.brewData()
        recipelist = ['coolkoelsh', 'maxhop', 'silverdollar']
        bd.setRecipeList(recipelist)
        bd.setCurrentRecipe('silverdollar')
        bd.setSelectedRecipe('silverdollar')
        status = {}
        status['name'] = 'silverdollar'
        status['stage'] = 'First'
        bd.setStatus(status)
        bd.setRunStatus('run')
        bd.setPause(False)

        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)

        driver.find_element_by_xpath("//a[2]/button").click()
 
        driver.find_element_by_xpath("//input[@value='Pause']").click()
        self.assertEqual(
            'Run Control\nCurrent Recipe: silverdollar\nCurrent Stage: First\nRun status: ' +
            'Paused\nStart/stop brewing program\nPause brewing process ' +
            'temporarily\nSkip one stage forward.\nClear error.\n\n\n' +
            'HomeRun ControlStatusStagesRecipeListRecipe',
            driver.find_element_by_css_selector("body").text)
        assert bd.getPause()
        driver.find_element_by_xpath("//input[@value='Resume']").click()
        self.assertEqual(
            'Run Control\nCurrent Recipe: silverdollar\nCurrent Stage: First\nRun status: ' +
            'Running\nStart/stop brewing program\nPause brewing process ' +
            'temporarily\nSkip one stage forward.\nClear error.\n\n\n' +
            'HomeRun ControlStatusStagesRecipeListRecipe',
            driver.find_element_by_css_selector("body").text)
        assert not bd.getPause()

    def test_Error(self):

        bd = dataMemcache.brewData()
        recipelist = ['coolkoelsh', 'maxhop', 'silverdollar']
        bd.setRecipeList(recipelist)
        bd.setCurrentRecipe('silverdollar')
        bd.setSelectedRecipe('silverdollar')
        status = {}
        status['name'] = 'silverdollar'
        status['stage'] = 'First'
        bd.setStatus(status)
        bd.setRunStatus('run')
        bd.setPause(False)
 
        driver = self.driver
        self.driver.get(self.url_base())
        # Make sure we start on home page
        self.assertTrue('Hopitty' in self.driver.title)
        bd.setError()

        driver.find_element_by_xpath("//a[2]/button").click()
        self.assertEqual(
            'Run Control\nCurrent Recipe: silverdollar\nCurrent Stage: First\nRun status: ' +
            'Paused\nStart/stop brewing program\nPause brewing process ' +
            'temporarily\nSkip one stage forward.\nClear error.\n\n\n' +
            'HomeRun ControlStatusStagesRecipeListRecipe',
            driver.find_element_by_css_selector("body").text)

        self.assertEqual("", driver.find_element_by_xpath("//input[@value='Skip']").text)
        self.assertEqual("", driver.find_element_by_xpath("//input[@value='Error']").text)
        #assert bd.getPause()
        
