import os
from pprint import pprint
#import appliances.myloader
#import ctrl.controllers
import ctrl.readRecipe
import ctrl.checkers


def testRecipeCheck():
    ctrl1 = ctrl.controllerList()
    ctrl1.load()
    print len(ctrl1)
    for key, c in ctrl1.items():
        print key

    here = os.getcwd()
    print here
    try:
        data = ctrl.readJson('src/tests/json_data')
    except:
        try:
            data = ctrl.readJson('tests/json_data')
        except:
            try:
                data = ctrl.readJson('tests/json_data')
            except:
                data = ctrl.readJson('json_data')
                print 'Could not find recipe'
    js = ctrl.jsonStages(data, ctrl1)
    stages = js.getStages()
    assert len(stages) > 0
    pprint(stages)
    assert ctrl.checkers.checkRecipe(ctrl1, stages, True)
    name = js.getRecipeName()
    print 'Name:', name
    assert len(name) > 0
#    assert isinstance(name, str)


def testcheck2():
    c = ctrl.controllerList()
    c.load()
    assert len(c) > 0
