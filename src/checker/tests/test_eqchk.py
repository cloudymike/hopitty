'''
Created on Apr 12, 2014

@author: mikael

testing of equipment checker, module eqchk
'''

import checker
import ctrl
import appliances


def myname():
    return(inspect.stack()[1][3])


def simpleCtrl():
    """
    Very simple controller for testingt
    """
    ctrl1 = ctrl.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl())
    return(ctrl1)


def simpleDict():
    """
    Simple stages to match simple controller, as dict
    """
    stages = {
        "1 stage": {
            "genctrl": {
                "active": True,
                "targetValue": 1
            }
        }
    }
    return(stages)


def simpleBadDict():
    """
    Simple stages to NOT match simple controller, as dict
    """
    stages = {
        "1 stage": {
            "bobbysue": {
                "active": True,
                "targetValue": 1
            }
        }
    }
    return(stages)


def simpleStages():
    """
    Simple stages to match simple controller, as string
    for reading with readRecipe
    """
    stages = """
{
"name":"IPA",
  "recipe":   {
    "1stage":{
      "genctrl":1
    }
  }
}
    """
    return(stages)


def test_instantiate():
    """
    Slightly silly test but a minimum to start with
    """
    a = checker.equipment()
    assert a is not None
    b = checker.equipment(simpleCtrl(), simpleDict())
    assert b is not None


def test_check_checkRecipeVsController():
    """
    Test that recipe and stages has to match
    """
    a = checker.equipment(simpleCtrl(), {})
    assert a.check()
    b = checker.equipment(simpleCtrl(), simpleDict())
    assert b.check()
    c = checker.equipment(simpleCtrl(), simpleBadDict())
    assert not c.check()


if __name__ == "__main__":

    test_instantiate()
    test_check_checkRecipeVsController()
    print "=====SUCCESS====="
