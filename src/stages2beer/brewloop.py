
import sys
import time
import ctrl
import json
#from threading import Thread
import threading
import dataMemcache as datastore
import stages2beer


class brewloop(threading.Thread):

    def __init__(self, controllers=None, loopdelay=0.1):
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
        self.sb = None

    def run(self):
        print "going"
        crumb = '.'
        while(not self._stopflag.isSet()):
            if self.myData.getTerminate():
                crumb = 't'
                self._stopflag.set()
            if self.sb is None:
                crumb = 's'
                if self.myData.getCtrlRunning():
                    self.sb = stages2beer.s2b(self.controllers,
                                              self.myData.getCurrentRecipe())
                    self.sb.start()
            if (self.sb is not None) and (not self.sb.isAlive()):
                crumb = 'S'
                self.sb = None
                self.myData.setCtrlRunning(False)
            if self.sb is not None:
                crumb = 'r'
                self.myData.setCurrentStage(self.sb.getStage())
                if self.myData.getSkip():
                    self.myData.setSkip(False)
                    self.sb.skip()

            sys.stdout.write(crumb)
            sys.stdout.flush()

            time.sleep(self.loopdelay)
        if self.sb is not None:
            self.sb.stop()
            self.sb.join()

    def stop(self):
        self._stopflag.set()

    def stopped(self):
        return not self.isAlive()
