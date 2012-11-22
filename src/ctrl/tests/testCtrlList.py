import appliances.boiler

import os
from pprint import pprint
import appliances.hoptimer
import appliances.hotWaterTun
import appliances.hwPump
import ctrl.controllers
import ctrl.readRecipe
import ctrl.simswitch
import appliances.circulationPump


def createCtrl():
    """Instantiate a list of all controllers"""
    #cirsw = ctrl.simswitch.simSwitch()
    #pumpsw = ctrl.simswitch.simSwitch()

    ctrl1 = ctrl.controllers()
    ctrl1.addController('genctrl', appliances.genctrl())
    ctrl1.addController('timer', appliances.hoptimer())
    ctrl1.addController('pump', appliances.hwPump())
    ctrl1.addController('circulationPump', appliances.circulationPump())
    ctrl1.addController('heater', appliances.hotWaterTun.hwtsim())
    ctrl1.addController('boiler', appliances.boiler())
    return(ctrl1)


def testReadStages():

    ctrl1=createCtrl()
    
    print os.getcwd()
    try:
        stages = ctrl.readRecipe.readRecipe('src/ctrl/tests/json_data',ctrl1)
    except:
        try:
            stages = ctrl.readRecipe.readRecipe('ctrl/tests/json_data',ctrl1)
        except:
            try:
                stages = ctrl.readRecipe.readRecipe('tests/json_data',ctrl1)
            except:
                stages = ctrl.readRecipe.readRecipe('json_data',ctrl1)
    assert len(stages) > 0
    pprint(stages)
    ctrlCount = len(ctrl1)
    print ctrlCount
    for s_key, s_val in stages.items():
        print s_key
        assert ctrlCount == len(s_val)

