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

import ctrl
import json


class s2b():

    def __init__(self, controllers):
        """
        Run equipment based on json file provided
        """
        self.controllers = None
        self.running = False
        self.paused = False
        self.verbose = False

        self.controllers = controllers

    def run(self, stages_json):
        #no blocking, I.e a separate thread
        pass

    def isRunning(self):
        return(False)

    def check(self, stages_json):
        """
        Simple check to validate that the recipe usees controllers
        in the controller list.
        """
        stages = json.loads(stages_json)
        return(ctrl.checkers.checkRecipe(self.controllers,
                                         stages,
                                         self.verbose))

    def quickRun(self, stages_json):
        return(False)

    def isError(self):
        return(False)

    def resetError(self):
        pass

    def setError(self):
        pass

    def pause(self):
        pass

    def unPause(self):
        pass

    def isPause(self):
        return(False)

    def skip(self):
        pass

    def stop(self):
        pass

    def getStatus(self):
        return({})

    def HWOK(self):
        return(False)

    def setLogOutput(self, file_handle):
        pass

    def getCtrl(self):
        return(self.controllers)

    def quickRecipe(self):
        """
        Runs through the recipe without any delay to just check it is OK
        This is different from check recipe in that it will also run
        each controller, thus test hardware if connected and not
        permissive
        """
        self.controllers.stop()
        for r_key, settings in sorted(self.stages.items()):
            self.controllers.run(settings)
            if True:
                print ""
                print "Stage: ", r_key
            if not ctrl.checkHardware(self.controllers):
                self.controllers.shutdown()
                return(False)
            self.controllers.stopCurrent(settings)
        return(True)
