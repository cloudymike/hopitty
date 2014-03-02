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

    def getStatus(self):
        try:
            status = self.getFromMemcache("hopitty_run_key")
        except:
            status = None
        if status is None:
            status = {}
        return(status)

    def setStatus(self, stages):
        """ Stores the status into memcache record """
        self.setToMemcache("hopitty_run_key", stages)

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

#    def getRunStatus(self):
#        """
#        Obsoleted, replaced with getCtrlRunning
#        Provided backwards compatibility but get value from getCtrlRunning
#        """
#        if self.getCtrlRunning():
#            return('run')
#        else:
#            return('stop')

    # This is data that should be sent to controller
#    def setRunStatus(self, value):
#        """
#        Obsoleted, replaced with setCtrlRunning
#        """
#        assert value in ['run', 'stop']
#        if value == 'run':
#            self.setCtrlRunning(True)
#        else:
#            self.setCtrlRunning(False)

    def getCurrentStage(self):
        if self.getCtrlRunning():
            status = self.getStatus()
            try:
                currentStage = status['stage']
            except:
                currentStage = ""
        else:
            currentStage = ""
        return(currentStage)

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
        stat = self.getStatus()
        if self.getCtrlRunning():
            try:
                recipe = stat['name']
            except:
                recipe = ""
        else:
            recipe = self.getFromMemcache('currentRecipe')
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

    def setHWerror(self, id='unknown', retries=5, errorText="HW error"):
        if not id in self.HWerrorDict:
            self.HWerrorDict[id] = 1
        else:
            self.HWerrorDict[id] = self.HWerrorDict[id] + 1
        if self.HWerrorDict[id] > retries:
            print "ERROR: ", errorText
            self.setError()
        print id, self.HWerrorDict[id]

    def unsetHWerror(self, id='unknown'):
        if not id in self.HWerrorDict:
            self.HWerrorDict[id] = 0
        else:
            self.HWerrorDict[id] = 0

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
