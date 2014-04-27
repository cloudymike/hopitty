"""
This is a glue layer between using s2b and the dataMemcache.
It is also controlling the run by interpreting the data.

This class will likely go away if we call s2b from within the web application
"""
import sys
import time
import ctrl
import json
#from threading import Thread
import threading
import dataMemcache as datastore
import stages2beer


class brewloop(threading.Thread):

    def __init__(self, controllers=None, recipelist=None, loopdelay=0.1):
        """
        A main daemon loop to run brewing
        Reads data from datastore/dataMemcache and acts on this
        Will start a stages2brew thread
        Takes input controllers that will be passed to s2b
        loopdelay is the time of sleep between restart of each loop
        Setting these may be important for testing
        """
        super(brewloop, self).__init__()
        self.controllers = controllers
        self.loopdelay = loopdelay
        self._stopflag = threading.Event()
        self.myData = datastore.brewData()
        self.sb = stages2beer.s2b()
        self.wasRunning = False
        self.verbose = True
        self.stages = {}
        self.recipelist = recipelist

    def run(self):
        crumb = '.'
        print "starting brewloop"
        self.wasRunning = False
        while(not self._stopflag.isSet()):
            if self.myData.getTerminate():
                """
                A terminate to this thread has been requested.
                Set flag and thread will terminate in next loop
                """
                crumb = 't'
                self._stopflag.set()
            if self.sb.isAlive():
                """
                Thread is running, read data and control thread
                This is the main activity section
                """
                self.wasRunning = True
                crumb = 'r'
                self.myData.setCurrentStage(self.sb.getStage())
                if self.myData.getSkip():
                    crumb = 'J'
                    self.myData.setSkip(False)
                    self.sb.skip()
                if self.myData.getPause():
                    self.sb.pause()
                    crumb = 'p'
                else:
                    self.sb.unpause()
            else:
                """
                s2b thread is stopped. Check if we need it is just stopped
                has been stopped for a while, if it needs to start
                """
                if self.wasRunning:
                    """
                    If thread just stopped, set CtrlRunning to False, else
                    read setCtrlRunning to see if it is time to start again.
                    """
                    crumb = 'S'
                    self.myData.setCtrlRunning(False)
                    self.wasRunning = False
                else:
                    crumb = 's'
                    """
                    s2b thead has been stopped for a while
                    """
                    if self.myData.getCtrlRunning():
                        """
                        A new start signal, restart the s2b thread
                        Make selected recipe current recipe
                        Kick off a new s2b
                        """
                        crumb = 'R'
                        recipeName = self.myData.getSelectedRecipe()
                        self.myData.setCurrentRecipe(recipeName)

                        try:
                            newrecipe = self.recipelist.getRecipe(recipeName)
                        except:
                            newrecipe = {}

                        self.sb = \
                            stages2beer.s2b(self.controllers,
                                            newrecipe)
                        self.sb.start()

            if self.verbose:
                sys.stdout.write(crumb)
                sys.stdout.flush()

            time.sleep(self.loopdelay)

        if self.sb.isAlive():
            self.sb.stop()
            self.sb.join()
        print ""
        print "brewloop stopped"

    def stop(self):
        self._stopflag.set()

    def stopped(self):
        return not self.isAlive()

    def setStages(self, stages):
        self.stages = stages.copy()
