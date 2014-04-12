# New version of runctrl that will
# structure the brew control process
#
# The objective is to keep this version of controller as simple as possible
# The input file is a simple stages list, and the controllers
# A check for controllers and json list matches but all other checks
# should be done outside of this module.
#
# In addition control functions are added to stop, pause and skip a step
# Help functions are included to get and check data.

import time
import ctrl
import json
#from threading import Thread
import threading


class s2b(threading.Thread):

    def __init__(self, controllers=None, stages=None):
        """
        Run equipment in controllers based on json file provided
        """
        super(s2b, self).__init__()

        self.verbose = False
        self.runOK = True
        self.currentStage = None

        self.pwait = threading.Event()
        self.pwait.set()

        self._stopflag = threading.Event()
        self._skipflag = threading.Event()

        self.controllers = controllers

        if isinstance(stages, dict):
            self.stages = stages
        else:
            self.stages = None

    def run(self):
        """
        Main run loop. Go through each stage of recipe and
        for each stage loop until all targets met.
        no blocking, I.e a separate thread
        """
        self.runOK = self.check()

        if not self.runOK:
            return

        for r_key, settings in sorted(self.stages.items()):
            self.currentStage = r_key
            self.controllers.stop()
            self.controllers.run(settings)
            skipone = False
            while ((not self.controllers.done()) and
                  (not self._stopflag.isSet()) and
                  (not skipone)):
                if self._skipflag.isSet():
                    skipone = True
                    self._skipflag.clear()
                else:
                    if self.paused():
                        self.controllers.pause(settings)
                    else:
                        self.controllers.run(settings)
                    time.sleep(0.5)

    def OK(self):
        return(self.runOK)

    def check(self):
        """
        Simple check to validate that the recipe uses controllers
        in the controller list.
        """
        if self.stages == {}:
            return(False)
        if self.controllers is None:
            return(False)
        if self.stages is not None:
            for r_key, settings in sorted(self.stages.items()):
                if not self.controllers.check(settings):
                    return(False)
            return(True)
        return(False)

    def quickRun(self):
        """
        Runs through the recipe without any delay to just check it is OK
        This is different from check recipe in that it will also run
        each controller, thus test hardware if connected and not
        permissive
        """
        self.controllers.stop()
        for r_key, settings in sorted(self.stages.items()):
            try:
                self.controllers.run(settings)
                self.controllers.stopCurrent(settings)
            except:
                return(False)
        return(True)

    def stop(self):
        self._stopflag.set()

    def stopped(self):
        return not self.isAlive()

    def pause(self):
        self.pwait.clear()

    def unpause(self):
        self.pwait.set()

    def paused(self):
        return not self.pwait.isSet()

    def skip(self):
        self._skipflag.set()

    def getCtrl(self):
        """
        Returns the controller dict object.
        Mostly for testing purposes
        """
        return(self.controllers)

    def getStages(self):
        """
        Returns all the stages read in
        Mostly for testing purposes
        """
        return(self.stages)

    def getStage(self):
        """
        Returns the current stage
        """
        return(self.currentStage)

    def getStatus(self):
        """
        Returns the status of the controllers
        This should be checked for thread safeness
        """
        statusNow = self.controllers.status()
        return(statusNow)

    def HWOK(self):
        return(self.controllers.HWOK())

#    def isError(self):
#        return(False)
#
#    def resetError(self):
#        pass
#
#    def setError(self):
#        pass
#
#    def printCrumb(self):
#        if myData.getError():
#            crumb = 'E'
#        elif myData.getPause():
#            crumb = 'P'
#        else:
#            crumb = '.'
#
#        sys.stdout.write(crumb)
#        sys.stdout.flush()
#        return({})
#
#    def setLogOutput(self, file_handle):
#        pass
