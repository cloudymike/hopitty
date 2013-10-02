'''
Created on Mar 19, 2013

@author: mikael
'''

import memcache
# @PydevCodeAnalysisIgnore


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
        if stages == None:
            stages = {}
        return(stages)

    def setStagesList(self, stages):
        """ Stores the stages data into memcache record """
        self.setToMemcache("stagesDict", stages)

    def getRecipeList(self):
        recipes = self.getFromMemcache('recipeNameList')
        if recipes == None:
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
        if status == None:
            status = {}
        return(status)

    def setStatus(self, stages):
        """ Stores the status into memcache record """
        self.setToMemcache("hopitty_run_key", stages)

    def getRunStatus(self):
        runStatus = self.getFromMemcache('runStatus')
        if runStatus == None:
            runStatus = ""
        return(runStatus)

    def getCurrentStage(self):
        if self.getRunStatus() == 'run':
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
        if self.getRunStatus() == 'run':
            try:
                recipe = stat['name']
            except:
                recipe = ""
        else:
            recipe = self.getFromMemcache('currentRecipe')
        return(recipe)

    def getSelectedRecipe(self):
        """
        Get the recipe that is selected on recipe lists page.
        This may differ from current recipe if brew is in progress
        When brew is stopped it should be the same
        """
        selected = self.getFromMemcache('selectedRecipe')
        return(selected)

    # This is data that should be sent to controller
    def setRunStatus(self, value):
        assert value in ['run', 'stop']
        self.setToMemcache('runStatus', value)

    def setCurrentRecipe(self, value):
        self.setToMemcache('currentRecipe', value)

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
        if pauseStatus == None:
            return(False)
        return(pauseStatus == 'True')

    def setError(self):
        self.setPause(True)
        self.setToMemcache('errorstatus', 'True')

    def unsetError(self):
        self.setToMemcache('errorstatus', 'False')

    def getError(self):
        errorStatus = self.getFromMemcache('errorstatus')
        if errorStatus == None:
            return(False)
        return(errorStatus == 'True')

    def setSkip(self, value):
        if value:
            self.setToMemcache('skip', 'True')
        else:
            self.setToMemcache('skip', 'False')

    def getSkip(self):
        skipStatus = self.getFromMemcache('skip')
        if skipStatus == None:
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
        if recipe == None:
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


# End of class brewData
def dummyRecipe(bd):
    bd.clearRecipe()
    bd.addToRecipe('Cascade', 1, 'dispenser1')
    bd.addToRecipe('Chocolate Malt', 8, 'mashtun')
    bd.addToRecipe('Pale Malt', 88, 'mashtun')
    return(bd.getRecipe())


def testRecipe():
    d1 = brewData()
    d2 = brewData()
    r0 = dummyRecipe(d1)
    r1 = d1.getRecipe()
    print r0
    print r1
    assert r0 == r1
    r2 = d2.getRecipe()
    print r2
    assert r0 == r2
    d2.addToRecipe('Crystal 40L', 4, 'mashtun')
    r1 = d1.getRecipe()
    r2 = d2.getRecipe()
    print r2
    assert len(r2) == len(r0) + 1
    assert r1 == r2
    assert r0 != r2

    c = d1.getRecipeContainers()
    print c
    assert len(c) > 0
    assert 'mashtun' in c
    if len(c) > 1:
        assert c[0] < c[1]

    mt = d1.getItemsInContainer('mashtun')
    print mt
    assert len(mt) > 0
    assert len(mt) < len(d1.getRecipe())
    print "OK"

if __name__ == "__main__":
    testRecipe()
