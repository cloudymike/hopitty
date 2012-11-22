import appliances.boiler

import os
from pprint import pprint
import appliances.genctrl
import appliances.hoptimer
import appliances.hotWaterTun
import appliances.hwPump
import ctrl.controllers
import ctrl.readRecipe
import ctrl.simswitch
import appliances.circulationPump


def createCtrl():
    """Instantiate a list of all controllers"""

    ctrl1 = ctrl.controllerList()
    ctrl1.addController('generic', appliances.genctrl())
    ctrl1.addController('timer', appliances.hoptimer())
    ctrl1.addController('pump', appliances.hwPump())
    ctrl1.addController('circulationPump', appliances.circulationPump())
    ctrl1.addController('heater', appliances.hotWaterTun.hwtsim())
    ctrl1.addController('boiler', appliances.boiler())
    return(ctrl1)


def testReadStages():
    ctrl1=createCtrl()
    here=os.getcwd()
    print here
    try:
        stages = ctrl.readRecipe('src/ctrl/tests/json_data',ctrl1)
    except:
        try:
            stages = ctrl.readRecipe('ctrl/tests/json_data',ctrl1)
        except:
            try:
                stages = ctrl.readRecipe('tests/json_data',ctrl1)
            except:
                stages = ctrl.readRecipe('json_data',ctrl1)
                print 'Could not find recipe'
    assert len(stages) > 0
    pprint(stages)
    ctrlCount = len(ctrl1)
    print ctrlCount
    for s_key, s_val in stages.items():
        print s_key
        assert ctrlCount == len(s_val)


