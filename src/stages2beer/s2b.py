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

        self.pwait = threading.Event()
        self.pwait.set()

        self._stopflag = threading.Event()

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
        if self.stages is None:
            return
        if self.stages == {}:
            return
        if self.controllers is None:
            return

        for r_key, settings in sorted(self.stages.items()):
            self.controllers.stop()
            self.controllers.run(settings)
            while ((not self.controllers.done()) and
                  (not self._stopflag.isSet())):
                self.pwait.wait()
                self.controllers.run(settings)
                time.sleep(0.5)

    def check(self):
        """
        Simple check to validate that the recipe uses controllers
        in the controller list.
        """
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

    def getCtrl(self):
        return(self.controllers)

    def getStages(self):
        return(self.stages)

    def isError(self):
        return(False)

    def resetError(self):
        pass

    def setError(self):
        pass

    def skip(self):
        pass

    def getStatus(self):
        return({})

    def HWOK(self):
        return(False)

    def setLogOutput(self, file_handle):
        pass
