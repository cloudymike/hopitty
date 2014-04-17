'''
Created on Mar 19, 2013

@author: mikael
'''

import memcache
# @PydevCodeAnalysisIgnore

import time


class brewData(object):
    '''
    Access funtions to brew data. As this is memcache based, we should
    not hold any data, but rather just have access functions to data stored
    in memcache.

    General form is setMyData and getMyData
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.recipe = []
        self.HWerrorDict = {}

    def getFromMemcache(self, key):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        try:
            value = mc.get(key)
        except:
            value = None
        return(value)

    def setToMemcache(self, key, value):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        mc.set(key, value)

    def getStagesList(self):
        stages = self.getFromMemcache('stagesDict')
        if stages is None:
            stages = {}
        return(stages)

    def setStagesList(self, stages):
        """ Stores the stages data into memcache record """
        self.setToMemcache("stagesDict", stages)

    def getRecipeList(self):
        recipes = self.getFromMemcache('recipeNameList')
        if recipes is None:
            recipes = []
        recipes.sort()
        return(recipes)

    def setRecipeList(self, recipes):
        """ Stores the status into memcache record """
        self.setToMemcache('recipeNameList', recipes)

    def setCtrlRunning(self, value):
        """
        Sets the run status of the controller (the brewer)
        This replaces previous RunStatus
        """
        self.setToMemcache('ctrlRunning', value)

    def getCtrlRunning(self):
        """
        Gets the runs status of the controller
        Returns boolean value True if running.
        """
        ctrlRunning = self.getFromMemcache('ctrlRunning')
        if ctrlRunning is None:
            ctrlRunning = False
            self.setCtrlRunning(False)
        return(ctrlRunning)

    def getCurrentStage(self):
        if self.getCtrlRunning():
            try:
                currentStage = self.getFromMemcache('currentStage')
            except:
                currentStage = ""
        else:
            currentStage = ""
        return(currentStage)

    def setCurrentStage(self, value):
        """
        Sets the run stage of the controller (the brewer)
        This replaces previous the use of setStatus
        """
        self.setToMemcache('currentStage', value)

    def getControllerList(self):
        controllerList = []
        stages = self.getStagesList()
        for stage, step in sorted(stages.items()):
            for ctrl, val in step.items():
                if ctrl not in controllerList:
                    controllerList.append(ctrl)
        return(controllerList)

# Use this in final production
    def getCurrentRecipe(self):
        try:
            recipe = self.getFromMemcache('currentRecipe')
        except:
            recipe = ""
        return(recipe)

    def setCurrentRecipe(self, value):
        self.setToMemcache('currentRecipe', value)

    def getSelectedRecipe(self):
        """
        Get the recipe that is selected on recipe lists page.
        This may differ from current recipe if brew is in progress
        When brew is stopped it should be the same
        """
        selected = self.getFromMemcache('selectedRecipe')
        return(selected)

# This is data that should be sent to controller
    def setSelectedRecipe(self, value):
        self.setToMemcache('selectedRecipe', value)

    def setPause(self, value):
        if value:
            self.setToMemcache('pause', 'True')
        else:
            self.setToMemcache('pause', 'False')

    def getPause(self):
        pauseStatus = self.getFromMemcache('pause')
        if pauseStatus is None:
            return(False)
        return(pauseStatus == 'True')

    def setError(self):
        self.setPause(True)
        self.setToMemcache('errorstatus', 'True')

    def unsetError(self):
        self.setToMemcache('errorstatus', 'False')

    def getError(self):
        errorStatus = self.getFromMemcache('errorstatus')
        if errorStatus is None:
            return(False)
        return(errorStatus == 'True')

    def setHWerror(self, myid='unknown', retries=5, errorText="HW error"):
        if not myid in self.HWerrorDict:
            self.HWerrorDict[myid] = 1
        else:
            self.HWerrorDict[myid] = self.HWerrorDict[myid] + 1
        if self.HWerrorDict[myid] > retries:
            print "ERROR: ", errorText
            self.setError()
        print myid, self.HWerrorDict[myid]

    def unsetHWerror(self, myid='unknown'):
        if not myid in self.HWerrorDict:
            self.HWerrorDict[myid] = 0
        else:
            self.HWerrorDict[myid] = 0

    def setSkip(self, value):
        if value:
            self.setToMemcache('skip', 'True')
        else:
            self.setToMemcache('skip', 'False')

    def getSkip(self):
        skipStatus = self.getFromMemcache('skip')
        if skipStatus is None:
            return(False)
        return(skipStatus == 'True')

    def setTerminate(self, value):
        """
        Hard terminate, stop all and exit.
        """
        if value:
            self.setToMemcache('terminate', 'True')
        else:
            self.setToMemcache('terminate', 'False')

    def getTerminate(self):
        """
        Hard terminate, if true stop all and exit.
        """
        skipStatus = self.getFromMemcache('terminate')
        if skipStatus is None:
            return(False)
        return(skipStatus == 'True')

    def addToRecipe(self, ingredience, amount, container, unit='oz'):
        recipe = self.getRecipe()
        recipeItem = [ingredience, amount, container, unit]
        recipe.append(recipeItem)
        self.setToMemcache('recipe', recipe)

    def clearRecipe(self):
        recipe = []
        self.setToMemcache('recipe', recipe)

    def getRecipe(self):
        recipe = self.getFromMemcache('recipe')
        if recipe is None:
            recipe = []
        return(recipe)

    def getRecipeContainers(self):
        r = self.getRecipe()
        c = []
        for ri in r:
            if not (ri[2] in c):
                c.append(ri[2])
        c.sort()
        return (c)

    def getItemsInContainer(self, container):
        r = self.getRecipe()
        c = []
        for ri in r:
            if ri[2] == container:
                c.append(ri)
        return(c)

    def resetWatchdog(self):
        watchdogTime = int(time.time())
        self.setToMemcache('watchdogTime', watchdogTime)

    def checkWatchdog(self):
        checkwatchdog = int(time.time())
        watchdogTime = self.getFromMemcache('watchdogTime')
        if watchdogTime is None:
            watchdogTime = 0
        retval = abs(watchdogTime - checkwatchdog) > 10
        return(retval)

    def setControllersStatus(self, dictval):
        self.setToMemcache('controllersStatus', dictval)

    def getControllersStatus(self):
        ctrlstat = self.getFromMemcache('controllersStatus')
        if ctrlstat is None:
            ctrlstat = {}
        return(ctrlstat)
