import os
from pprint import pprint
import appliances.myloader
import ctrl.controllers
import ctrl.readRecipe
import ctrl.checkers


def testRecipeCheck():
    ctrl1=ctrl.controllerList()
    ctrl1.load()
    print len(ctrl1)
    for key, c in ctrl1.items():
        print key

    here=os.getcwd()
    print here
    try:
        stages = ctrl.readRecipe('src/tests/json_data',ctrl1)
    except:
        try:
            stages = ctrl.readRecipe('tests/json_data',ctrl1)
        except:
            try:
                stages = ctrl.readRecipe('tests/json_data',ctrl1)
            except:
                stages = ctrl.readRecipe('json_data',ctrl1)
                print 'Could not find recipe'
    assert len(stages) > 0
    pprint(stages)
    assert ctrl.checkers.checkRecipe(ctrl1, stages, True)


def testcheck2():
    c = ctrl.controllerList()
    c.load()
    assert len(c) > 0