#!/usr/bin/python

import json
from pprint import pprint
import time
import genctrl
import hoptimer
import hotWaterTun
import hwPump
import controllers


def createCtrl():
    """Instantiate a list of all controllers"""
    ctrl = controllers.controllers()
    ctrl.addController(genctrl.genctrl())
    ctrl.addController(hoptimer.hoptimer_sim())
    ctrl.addController(hwPump.hwPump())
    ctrl.addController(hotWaterTun.hwtsim(None))
    return(ctrl)

json_data=open('json_data')

data = json.load(json_data)
#pprint(data)
json_data.close()

print "Recipe name:",data['name']

stages = {}
controllers=createCtrl()
recipe=data['recipe']
for stage, step in recipe.items():
#    print stage
    settings = {}
    # Set all controllers to inactive
    for c_key,c in controllers.items():
        s = {}
        s['targetValue']=0
        s['active']=False
        settings[c_key]=s
    # Activate and set target value for controllers that are in json
    for s_key,s_val in step.items():
#        print "    ", s_key, "	",s_val
        t = {}
        t['targetValue']=s_val
        t['active']=True
        settings[s_key]=t
    stages[stage]=settings

pprint(stages)
        

