
import os
from pprint import pprint
import ctrl.genctrl
import ctrl.hoptimer
import ctrl.hotWaterTun
import ctrl.hwPump
import ctrl.controllers
import ctrl.readRecipe
import ctrl.simswitch
import ctrl.circulationPump


def createCtrl():
    """Instantiate a list of all controllers"""
    cirsw = ctrl.simswitch.simSwitch()
    pumpsw = ctrl.simswitch.simSwitch()

    ctrl1 = ctrl.controllers.controllers()
    ctrl1.addController('genctrl', ctrl.genctrl.genctrl())
    ctrl1.addController('timer', ctrl.hoptimer.hoptimer())
    ctrl1.addController('pump', ctrl.hwPump.hwPump(pumpsw))
    ctrl1.addController('circulationPump', ctrl.circulationPump.circulationPump(cirsw))
    ctrl1.addController('heater', ctrl.hotWaterTun.hwtsim(None))
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

