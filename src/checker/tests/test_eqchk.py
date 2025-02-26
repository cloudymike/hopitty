'''
Created on Apr 12, 2014

@author: mikael

testing of equipment checker, module eqchk
'''
import inspect
import checker.equipment
import ctrl.controllers
import appliances.genctrl
import appliances.hoptimer
import appliances.boiler
import appliances.circulationPump
import appliances.hotWaterTun
import appliances.hwPump


def printMyname():
    print("....................", inspect.stack()[1][3])


def simpleCtrl():
    """
    Very simple controller for testingt
    """
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl.genctrl())
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


def mediumCtrl():
    """Instantiate a list of several controllers"""
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl.genctrl())
    ctrl1.addController('timer', appliances.hoptimer.hoptimer())
    ctrl1.addController('hotWaterPump', appliances.hwPump.hwPump())
    ctrl1.addController('circulationPump', appliances.circulationPump.circulationPump())
    ctrl1.addController('wortPump', appliances.hwPump.wortPump())
    ctrl1.addController('waterHeater', appliances.hotWaterTun.hwt())
    ctrl1.addController('boiler', appliances.boiler.boiler())
    return(ctrl1)


def test_instantiate():
    """
    Slightly silly test but a minimum to start with
    """
    a = checker.equipment.equipment()
    assert a is not None
    b = checker.equipment.equipment(simpleCtrl(), simpleDict())
    assert b is not None
    printMyname()


def test_check_checkRecipeVsController():
    """
    Test that recipe and stages has to match
    """
    a = checker.equipment.equipment(simpleCtrl(), {})
    assert a.check()
    b = checker.equipment.equipment(simpleCtrl(), simpleDict())
    assert b.check()
    c = checker.equipment.equipment(simpleCtrl(), simpleBadDict())
    assert not c.check()
    printMyname()


def test_checkBoilVolume():
    a = checker.equipment.equipment(simpleCtrl(), simpleDict())
    assert a.check()

    s1 = {"1s": {"wortPump": {"active": True, "targetValue": 1.0}}}
    b = checker.equipment.equipment(mediumCtrl(), s1)
    assert b.check()

    c = checker.equipment.equipment(mediumCtrl(), s1)
    c.updateEquipmentItem('boilerVolumeMax', 0.5)
    assert not c.check()

    s2 = {"1": {"wortPump": {"active": True, "targetValue": 1.0}},
          "2": {"wortPump": {"active": True, "targetValue": 1.0}}}
    d = checker.equipment.equipment(mediumCtrl(), s2)
    assert d.check()

    e = checker.equipment.equipment(mediumCtrl(), s2)
    e.updateEquipmentItem('boilerVolumeMax', 1.5)
    assert not e.check()
    printMyname()


def test_checkHotwaterVolume():
    a = checker.equipment.equipment(simpleCtrl(), simpleDict())
    assert a.check()

    s = {"1s": {"hotWaterPump": {"active": True, "targetValue": 1.0}}}
    b = checker.equipment.equipment(mediumCtrl(), s)
    assert b.check()

    c = checker.equipment.equipment(mediumCtrl(), s)
    c.updateEquipmentItem('maxTotalInVol', 0.5)
    assert not c.check()

    t = {"1": {"hotWaterPump": {"active": True, "targetValue": 1.0}},
         "2": {"hotWaterPump": {"active": True, "targetValue": 1.0}}}
    d = checker.equipment.equipment(mediumCtrl(), t)
    assert d.check()

    e = checker.equipment.equipment(mediumCtrl(), t)
    e.updateEquipmentItem('maxTotalInVol', 1.5)
    assert not e.check()
    printMyname()


def test_checkHotwaterHeaterVolume():
    a = checker.equipment.equipment(simpleCtrl(), simpleDict())
    assert a.check()

    s = {"1s": {"hotWaterPump": {"active": True, "targetValue": 1.0}}}
    b = checker.equipment.equipment(mediumCtrl(), s)
    assert b.check()

    c = checker.equipment.equipment(mediumCtrl(), s)
    c.updateEquipmentItem('maxInfusionVol', 0.5)
    assert c.check()

    s2 = {"1hw": {"hotWaterPump": {"active": True, "targetValue": 1.0},
                  "waterHeater": {"active": True, "targetValue": 165}}}
    c2 = checker.equipment.equipment(mediumCtrl(), s2)
    c2.updateEquipmentItem('maxInfusionVol', 0.5)
    assert not c2.check()

    printMyname()


def test_checkBoilerAndWaterHeater():
    """
    Test that boiler and water heater is not on at the same time
    For initial equipment that would use too much electrical power
    """
    sa = {"1s": {"waterHeater": {"active": True, "targetValue": 165}}}
    a = checker.equipment.equipment(mediumCtrl(), sa)
    assert a.check()

    sb = {"1s": {"boiler": {"active": True, "targetValue": 165}}}
    b = checker.equipment.equipment(mediumCtrl(), sb)
    assert b.check()

    sc = {"1s": {"waterHeater": {"active": True, "targetValue": 165},
                 "boiler": {"active": True, "targetValue": 165}}}
    c = checker.equipment.equipment(mediumCtrl(), sc)
    assert not c.check()

    printMyname()


def test_checkPumpsNoOverlap():
    """
    Test that recipe and stages has to match
    """
    sa = {"1s": {"hotWaterPump": {"active": True, "targetValue": 1}}}
    a = checker.equipment.equipment(mediumCtrl(), sa)
    assert a.check()

    sb = {"1s": {"wortPump": {"active": True, "targetValue": 1}}}
    b = checker.equipment.equipment(mediumCtrl(), sb)
    assert b.check()

    sc = {"1s": {"circulationPump": {"active": True, "targetValue": 1}}}
    c = checker.equipment.equipment(mediumCtrl(), sc)
    assert c.check()

    sd = {"1s": {"hotWaterPump": {"active": True, "targetValue": 1},
                 "wortPump": {"active": True, "targetValue": 1}}}
    d = checker.equipment.equipment(mediumCtrl(), sd)
    assert not d.check()

    se = {"1s": {"hotWaterPump": {"active": True, "targetValue": 1},
                 "circulationPump": {"active": True, "targetValue": 1}}}
    e = checker.equipment.equipment(mediumCtrl(), se)
    assert not e.check()

    printMyname()


def test_template():
    """
    Test template
    """
    sa = {"1s": {"waterHeater": {"active": True, "targetValue": 165}}}
    a = checker.equipment.equipment(mediumCtrl(), sa)
    assert a._equipment__checkBoilerAndWaterHeater()
    printMyname()


if __name__ == "__main__":
    test_checkPumpsNoOverlap()
    test_checkBoilerAndWaterHeater()

    test_instantiate()
    test_check_checkRecipeVsController()
    test_checkBoilVolume()
    test_checkHotwaterVolume()
    test_checkHotwaterHeaterVolume()

    print("=====SUCCESS!=====")
