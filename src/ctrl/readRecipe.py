#!/usr/bin/python

import json


def readJson(jsonFile):
    json_data = open(jsonFile)
    data = json.load(json_data)
    json_data.close()
    return(data)


def readName(data):
    name = data['name']
    print 'Name', name
    return(name)


def readRecipe(data, controllers):
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
