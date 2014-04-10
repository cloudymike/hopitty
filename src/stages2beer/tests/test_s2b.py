import json
import stages2beer
import ctrl
import appliances
import recipeReader


def simpleCtrl():
    ctrl1 = ctrl.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl())
    return(ctrl1)


def simpleStages():
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


def sStages():
    stages = """
{
    "1 stage":{
      "genctrl":1
    }
}
    """
    return(stages)


def mediumCtrl():
    """Instantiate a list of several controllers"""
    ctrl1 = ctrl.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl())
    ctrl1.addController('timer', appliances.hoptimer())
    ctrl1.addController('pump', appliances.hwPump())
    ctrl1.addController('circulationPump', appliances.circulationPump())
    ctrl1.addController('heater', appliances.hotWaterTun.hwt())
    ctrl1.addController('boiler', appliances.boiler())
    return(ctrl1)


def timerCtrl():
    """Instantiate a list of several controllers"""
    ctrl1 = ctrl.controllerList()
    ctrl1.addController('timer', appliances.hoptimer())
    return(ctrl1)


def test_instantiate():
    a = stages2beer.s2b()
    assert a is not None


def test_controllerInstantiate():
    a = stages2beer.s2b(None)
    assert a.getCtrl() is None
    b = stages2beer.s2b(simpleCtrl())
    assert isinstance(b.getCtrl(), dict)
    assert 'genctrl' in b.getCtrl()


def test_simpleStages():
    stages = sStages()
    a = stages2beer.s2b(simpleCtrl(), stages)
    a.check()


def test_basicThread():
    """
    Basic testing that the thread is working
    """
    a = stages2beer.s2b(None)
    a.start()
    assert a.isAlive()
    a.join()
    assert not a.isAlive()
    print "Yep, it finished"


def test_quickRun():
    r = recipeReader.jsonStages(simpleStages(), simpleCtrl())
    a = stages2beer.s2b(simpleCtrl(), r.getStages())
    assert a.quickRun()


def test_check():
    r = recipeReader.jsonStages(simpleStages(), simpleCtrl())
    a = stages2beer.s2b(simpleCtrl(), r.getStages())
    assert a.check()


def test_getStages():
    """
    Try different input format for stages
       dict
       json string
       json from recipeReader
    """
    pass


if __name__ == "__main__":
    test_instantiate()
    test_controllerInstantiate()
    test_simpleStages()
    test_basicThread()
    test_quickRun()
    test_check()
    test_getStages()
    print "All is good"
