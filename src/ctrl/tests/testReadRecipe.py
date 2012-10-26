
import json
from pprint import pprint
import time
import ctrl.genctrl
import ctrl.hoptimer
import ctrl.hotWaterTun
import ctrl.hwPump
import ctrl.controllers
import ctrl.readRecipe
import ctrl.controllers


def createCtrl():
    """Instantiate a list of all controllers"""
    ctrl1 = ctrl.controllers.controllers()
    ctrl1.addController('generic', ctrl.genctrl.genctrl())
    ctrl1.addController('timer', ctrl.hoptimer.hoptimer_sim())
    ctrl1.addController('pump', ctrl.hwPump.hwPump_sim())
    ctrl1.addController('heater', ctrl.hotWaterTun.hwtsim(None))
    return(ctrl1)


def testReadStages():
    ctrl1=createCtrl()
    try:
        stages = ctrl.readRecipe.readRecipe('ctrl/tests/json_data',ctrl1)
    except:
        try:
            stages = ctrl.readRecipe.readRecipe('tests/json_data',ctrl1)
        except:
            stages = ctrl.readRecipe.readRecipe('json_data',ctrl1)
            print 'Could not find recipe'
    assert len(stages) > 0
    pprint(stages)
    ctrlCount = len(ctrl1)
    print ctrlCount
    for s_key, s_val in stages.items():
        assert ctrlCount == len(s_val)


