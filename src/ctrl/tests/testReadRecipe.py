import appliances.boiler

import os
from pprint import pprint
import appliances.genctrl
import appliances.hoptimer
import appliances.hotWaterTun
import appliances.hwPump
import ctrl.controllers
import ctrl
import appliances.circulationPump
import recipeReader.readRecipe


def createCtrl():
    """Instantiate a list of all controllers"""

    ctrl1 = ctrl.controllerList()
    ctrl1.addController('generic', appliances.genctrl())
    ctrl1.addController('timer', appliances.hoptimer())
    ctrl1.addController('pump', appliances.hwPump())
    ctrl1.addController('circulationPump', appliances.circulationPump())
    ctrl1.addController('heater', appliances.hotWaterTun.hwt())
    ctrl1.addController('boiler', appliances.boiler())
    return(ctrl1)


def testReadStages():
    ctrl1 = createCtrl()
    here = os.getcwd()
    print here
    try:
        js = recipeReader.readRecipe.jsonStages('src/ctrl/tests/json_data', ctrl1)
    except:
        try:
            js = recipeReader.readRecipe.jsonStages('ctrl/tests/json_data', ctrl1)
        except:
            try:
                js = recipeReader.readRecipe.jsonStages('tests/json_data', ctrl1)
            except:
                js = recipeReader.readRecipe.jsonStages('json_data', ctrl1)
    #js = ctrl.jsonStages(data, ctrl1)
    stages = js.getStages()
    assert len(stages) > 0
    pprint(stages)
    ctrlCount = len(ctrl1)
    print ctrlCount
    for s_key, s_val in stages.items():
        print s_key
        assert ctrlCount == len(s_val)
