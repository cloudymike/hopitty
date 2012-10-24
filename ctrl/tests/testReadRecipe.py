
import json
from pprint import pprint
import time
import genctrl
import hoptimer
import hotWaterTun
import pump
import controllers
import readRecipe


def createCtrl():
    """Instantiate a list of all controllers"""
    ctrl = controllers.controllers()
    ctrl.addController(genctrl.genctrl())
    ctrl.addController(hoptimer.hoptimer_sim())
    ctrl.addController(pump.hwPump_sim())
    ctrl.addController(hotWaterTun.hwtsim(None))
    return(ctrl)


def testReadStages():
    ctrl=createCtrl()
    try:
        stages = readRecipe.readRecipe('ctrl/tests/json_data',ctrl)
    except:
        try:
            stages = readRecipe.readRecipe('tests/json_data',ctrl)
        except:
            stages = {}
            print 'Could not find recipe'
    assert len(stages) > 0
    pprint(stages)
    ctrlCount = len(ctrl)
    print ctrlCount
    for s_key, s_val in stages.items():
        assert ctrlCount == len(s_val)


