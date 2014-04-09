# TODO
# Check validity of json vs controller

import json


class jsonStages():
    """
    This class will wrap all the json functions. On instantiation, the
    object needs to be passed an json file and a controller list.
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

        if self.valid:
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
        print data
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
        #for c_key, c in controllers.items():
        for c_key in controllers.keys():
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
