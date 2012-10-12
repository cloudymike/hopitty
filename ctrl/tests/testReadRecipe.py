
import json
from pprint import pprint
import time
import genctrl
import hoptimer
import hotWaterTun
import hwPump
import controllers
import readRecipe


def createCtrl():
    """Instantiate a list of all controllers"""
    ctrl = controllers.controllers()
    ctrl.addController(genctrl.genctrl())
    ctrl.addController(hoptimer.hoptimer_sim())
    ctrl.addController(hwPump.hwPump())
    ctrl.addController(hotWaterTun.hwtsim(None))
    return(ctrl)


def testReadStages():
    ctrl=createCtrl()
    stages = readRecipe.readRecipe('tests/json_data',ctrl)
    assert len(stages) > 0
    pprint(stages)
    ctrlCount = len(ctrl)
    print ctrlCount
    for s_key, s_val in stages.items():
        assert ctrlCount == len(s_val)


