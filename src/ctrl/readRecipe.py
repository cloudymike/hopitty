#!/usr/bin/python

import json
#from collections import OrderedDict
#from pprint import pprint
#import time
#import appliances.genctrl
#import appliances.hoptimer
#import appliances.hotWaterTun
#import appliances.hwPump
#import controllers


def readRecipe(jsonFile, controllers):
    json_data = open(jsonFile)
    data = json.load(json_data)
    json_data.close()

    stages = {}
    recipe = data['recipe']
    for stage, step in recipe.items():
        settings = {}
        # Set all controllers to inactive
        for c_key, c in controllers.items():
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
