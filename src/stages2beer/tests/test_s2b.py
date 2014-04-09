import stages2beer
import ctrl
import appliances


def simpleCtrl():
    ctrl1 = ctrl.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl())
    return(ctrl1)


def simpleStages():
    stages = """
{
"name":"IPA",
  "recipe":   {
    "1":{
      "genctrl":1
    }
  }
}
    """
    return(stages)


def sStages():
    stages = """
{
    "1":{
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


def test_instantiate():
    a = stages2beer.s2b(None)
    assert a is not None


def test_controllerInstantiate():
    a = stages2beer.s2b(None)
    assert a.getCtrl() is None
    b = stages2beer.s2b(simpleCtrl())
    assert isinstance(b.getCtrl(), dict)
    assert 'genctrl' in b.getCtrl()


def test_simpleStages():
    a = stages2beer.s2b(simpleCtrl())
    a.check(sStages())


if __name__ == "__main__":
    test_instantiate()
    test_controllerInstantiate()
    test_simpleStages()
    print "All is good"
