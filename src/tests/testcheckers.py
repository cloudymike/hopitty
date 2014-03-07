import os
from pprint import pprint
#import appliances.myloader
#import ctrl.controllers
import ctrl
import ctrl.checkers
import recipeReader
import appliances


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


def testRecipeCheck():
    ctrl1 = createCtrl()
    #ctrl1 = ctrl.controllerList()
    #ctrl1.load()

    print len(ctrl1)
    for key, c in ctrl1.items():
        print key

    here = os.getcwd()
    print here
    try:
        js = recipeReader.jsonStages('src/ctrl/tests/json_data', ctrl1)
    except:
        try:
            js = recipeReader.jsonStages('ctrl/tests/json_data', ctrl1)
        except:
            try:
                js = recipeReader.jsonStages('tests/json_data', ctrl1)
            except:
                js = recipeReader.jsonStages('json_data', ctrl1)
    #js = ctrl.jsonStages(data, ctrl1)
    stages = js.getStages()
    assert len(stages) > 0
    print "========================"
    pprint(stages)
    print "========================"
    assert ctrl.checkers.checkRecipe(ctrl1, stages, True)
    name = js.getRecipeName()
    print 'Name:', name
    assert len(name) > 0
#    assert isinstance(name, str)


def testcheck2():
    c = ctrl.controllerList()
    c.load()
    assert len(c) > 0
