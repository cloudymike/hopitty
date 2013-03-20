'''
Created on Mar 19, 2013

@author: mikael
'''

import memcache
#@PydevCodeAnalysisIgnore


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
    def getFromMemcache(self, key):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        try:
            value = mc.get(key)
        except:
            value = None
        return(value)

    def getStagesList(self):
        stages = self.getFromMemcache('stagesDict')
        if stages == None:
            stages = {}
        return(stages)

    def getRecipeList(self):
        recipes = self.getFromMemcache('recipeNameList')
        if recipes == None:
            recipes = []
        recipes.sort()
        return(recipes)

    def getStatus(self):
        try:
            status = self.getFromMemcache("hopitty_run_key")
        except:
            status = None
        if status == None:
            status = []
        return(status)

    def getRunStatus(self):
        runStatus = self.getFromMemcache('runStatus')
        if runStatus == None:
            runStatus = ""
        return(runStatus)

    def getCurrentStage(self):
        status = self.getStatus()
        try:
            currentStage = status['stage']
        except:
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
        try:
            recipe = stat['name']
        except:
            recipe = ""
        return(recipe)
