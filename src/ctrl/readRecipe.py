#!/usr/bin/python
# TODO
# Check validity of json vs controller

import json


def readJson(jsonFile):
    json_data = open(jsonFile)
    data = json.load(json_data)
    json_data.close()
    return(data)


#def readName(data):
#    name = data['name']
#    return(name)


#def readRecipe(data, controllers):
#    stages = {}
#    recipe = data['recipe']
#    for stage, step in recipe.items():
#        settings = {}
        # Set all controllers to inactive
#        for c_key, c in controllers.items():
#            s = {}
#            s['targetValue'] = 0
#            s['active'] = False
#            settings[c_key] = s
        # Activate and set target value for controllers that are in json
#        for s_key, s_val in step.items():
#            t = {}
#            t['targetValue'] = s_val
#            t['active'] = True
#            settings[s_key] = t
#        stages[stage] = settings
#    return(stages)


class jsonStages():
    """
    This class will wrap all the bsmx functions. On instantiation, the
    object needs to be passed an xml file and a controller list.
    The strings in the controller list needs to match the strings in the json
    If the json file is not a valid recipe, and can not be brewed with the
    controllers, then the validRecipe will be false and any return of
    a stages list will be an empty list.
    """
    def __init__(self, json, controllerList):
        self.valid = False
        self.stages = {}
        self.ctrlList = []

        try:
            self.jsonDict = self.readJson(json)
            self.valid = True
        except:
            if isinstance(json, dict):
                self.jsonDict = json
                self.valid = True
            else:
                self.jsonDict = {}
                self.valid = False

        try:
            self.ctrlList = self.mkControllerList(controllerList)
        except:
            if isinstance(controllerList, list):
                self.ctrlList = controllerList
            else:
                self.ctrlList = []

        self.stages = self.readRecipe(self.jsonDict, self.ctrlList)

        if self.valid:
            self.valid = self.validateRecipe()

    def __del__(self):
        pass

    def getStages(self):
        """
        Returns a valid stages dictionary for the recipe
        """
        return(self.stages)

    def getRecipeName(self):
        return(self.readName(self.jsonDict))

    def isValid(self):
        return(self.valid)

    def validateRecipe(self):
        retval = True
        for s_key, stage in self.stages.items():
            for c_key, ctrlType in stage.items():
                if not c_key in self.ctrlList:
                    retval = False
        return(retval)

    def readRecipe(self, data, controllerList):
        stages = {}
        recipe = data['recipe']
        for stage, step in recipe.items():
            settings = {}
            # Set all controllers to inactive
            for c_key in controllerList:
                s = {}
                s['targetValue'] = 0
                s['active'] = False
                settings[c_key] = s
            # Activate and set target value for controllers that are in json
            for s_key, s_val in step.items():
                t = {}
                t['targetValue'] = s_val
                t['active'] = True
                settings[s_key] = t
            stages[stage] = settings
        return(stages)

    def mkControllerList(self, controllers):
        ctrlLst = []
        for c_key, c in controllers.items():
            ctrlLst.append(c_key)
        return(ctrlLst)

    def readJson(self, jsonFile):
        json_data = open(jsonFile)
        data = json.load(json_data)
        json_data.close()
        return(data)

    def readName(self, data):
        name = data['name']
        return(name)


#========== Start of test code =============


def m2Recipe():
    retDict = {
        "name": "IPA",
        "recipe":  {
            "4step": {
                "wortPump": 1.0
                }
            }
        }
    return(retDict)


def badRecipe():
    retDict = {
        "name": "IPA",
        "recipe":  {
            "4step": {
                "thingimajing": 1.0
                }
            }
        }
    return(retDict)


def ctrlDummyList():
    retlst = ['wortPump', 'boiler']
    return(retlst)


def ctrlDummyDict():
    retlst = {'wortPump': 'dummy1', 'boiler': 'dummy2'}
    return(retlst)


def test_m2Read():
    js = jsonStages(m2Recipe(), ctrlDummyList())
    assert js.getRecipeName() == "IPA"
    stages = js.getStages()
    assert stages["4step"] is not None
    oneStage = stages["4step"]
    assert oneStage is not None
    oneAction = oneStage["wortPump"]
    assert oneAction is not None
    assert oneAction['active']
    assert oneAction['targetValue'] == 1.0
    assert js.isValid()

    print "ok"


def test_m2ReadCtrlDict():
    js = jsonStages(m2Recipe(), ctrlDummyDict())
    assert js.getRecipeName() == "IPA"
    stages = js.getStages()
    assert stages["4step"] is not None
    oneStage = stages["4step"]
    assert oneStage is not None
    oneAction = oneStage["wortPump"]
    assert oneAction is not None
    assert oneAction['active']
    assert oneAction['targetValue'] == 1.0
    assert js.isValid()

    print "ok"


def test_badRecipeRead():
    js = jsonStages(badRecipe(), ctrlDummyList())
    assert js.getRecipeName() == "IPA"
    stages = js.getStages()
    assert stages["4step"] is not None
    oneStage = stages["4step"]
    assert oneStage is not None
    oneAction = oneStage["thingimajing"]
    assert oneAction is not None
    assert oneAction['active']
    assert oneAction['targetValue'] == 1.0
    assert not js.isValid()

    print "ok"


def test_wortpumptest():
    js = jsonStages("../../recipe/wort_pump_test", ctrlDummyList())
    assert js.getRecipeName() == "wort_pump_test"
    stages = js.getStages()
    assert stages["01"] is not None
    oneStage = stages["01"]
    assert oneStage is not None
    oneAction = oneStage["wortPump"]
    assert oneAction is not None
    assert oneAction['active']
    assert js.isValid()
    print "ok"


if __name__ == "__main__":
    test_m2Read()
    test_wortpumptest()
    test_badRecipeRead()
    test_m2ReadCtrlDict()
