import json
import stages2beer.s2b
import ctrl.controllers
import appliances.genctrl
import appliances.hoptimer
import appliances.boiler
import appliances.circulationPump
import appliances.hotWaterTun
import appliances.hwPump
import recipeReader.readRecipe
import inspect
import time


def myname():
    return(inspect.stack()[1][3])


def simpleCtrl():
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl.genctrl())
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


def simpleDict():
    stages = {
        "1 stage": {
            "genctrl": {
                "active": True,
                "targetValue": 1
            }
        }
    }
    return(stages)


def timerDict():
    td = {
        "1 stage": {
            "timer": {
                "active": True,
                "targetValue": 0.01
            }
        }
    }
    return td


def multiTimerDict():
    td = {
        "1 stage": {
            "timer": {
                "active": True,
                "targetValue": 0.01
            }
        },
        "2 stage": {
            "timer": {
                "active": True,
                "targetValue": 0.01
            }
        },
        "3 stage": {
            "timer": {
                "active": True,
                "targetValue": 0.01
            }
        }
    }
    return td


def mediumCtrl():
    """Instantiate a list of several controllers"""
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl.genctrl())
    ctrl1.addController('timer', appliances.hoptimer.hoptimer())
    ctrl1.addController('pump', appliances.hwPump.hwPump())
    ctrl1.addController('circulationPump', appliances.circulationPump.circulationPump())
    ctrl1.addController('heater', appliances.hotWaterTun.hwt())
    ctrl1.addController('boiler', appliances.boiler.boiler())
    return(ctrl1)


def timerCtrl():
    """Instantiate a list of several controllers"""
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.addController('timer', appliances.hoptimer.hoptimer())
    return(ctrl1)


def test_instantiate():
    a = stages2beer.s2b.s2b()
    assert a is not None
    print(myname(), "OK")


def test_controllerInstantiate():
    a = stages2beer.s2b.s2b(None)
    assert a.getCtrl() is None
    b = stages2beer.s2b.s2b(simpleCtrl())
    assert isinstance(b.getCtrl(), dict)
    assert 'genctrl' in b.getCtrl()
    print(myname(), "OK")


def test_simpleStages():
    stages = simpleDict()
    a = stages2beer.s2b.s2b(simpleCtrl(), stages)
    a.check()
    print(myname(), "OK")


def test_basicThread():
    """
    Basic testing that the thread is working
    """
    a = stages2beer.s2b.s2b(simpleCtrl(), simpleDict())
    a.start()
    assert a.isAlive()
    a.stop()
    a.join()
    assert not a.isAlive()
    print(myname(), "OK")


def test_ThreadEdgeCases():
    a = stages2beer.s2b.s2b(None, None)
    a.start()
    time.sleep(0.1)
    assert not a.isAlive()

    b = stages2beer.s2b.s2b(simpleCtrl(), None)
    b.start()
    time.sleep(0.1)
    assert not b.isAlive()

    c = stages2beer.s2b.s2b(simpleCtrl(), {})
    c.start()
    time.sleep(0.1)
    assert not c.isAlive()

    d = stages2beer.s2b.s2b(None, simpleDict())
    d.start()
    time.sleep(0.1)
    assert not d.isAlive()

    print(myname(), "OK")


def test_quickRun():
    r = recipeReader.readRecipe.jsonStages(simpleStages(), simpleCtrl())
    a = stages2beer.s2b.s2b(simpleCtrl(), r.getStages())
    assert a.quickRun()
    print(myname(), "OK")


def test_check():
    r = recipeReader.readRecipe.jsonStages(simpleStages(), simpleCtrl())
    a = stages2beer.s2b.s2b(simpleCtrl(), r.getStages())
    assert a.check()
    print(myname(), "OK")


def test_getStages():
    """
    Try different input format for stages and read them back.
       json from recipeReader
       json string
       dict
    """
    r1 = recipeReader.readRecipe.jsonStages(simpleStages(), simpleCtrl())
    a1 = stages2beer.s2b.s2b(simpleCtrl(), r1.getStages())
    stages1 = a1.getStages()
    assert isinstance(stages1, dict)
    assert '1stage' in stages1
    assert 'name' not in stages1

    a2 = stages2beer.s2b.s2b(simpleCtrl(), simpleDict())
    stages2 = a2.getStages()
    assert isinstance(stages2, dict)
    assert '1 stage' in stages2
    assert 'name' not in stages2

    a4 = stages2beer.s2b.s2b(simpleCtrl(), timerDict())
    stages4 = a4.getStages()
    assert isinstance(stages4, dict)
    assert '1 stage' in stages4
    assert 'name' not in stages4
    print(myname(), "OK")


def test_runShortTimer():
    a = stages2beer.s2b.s2b(timerCtrl(), timerDict())
    a.start()
    assert a.isAlive()
    a.join()
    assert not a.isAlive()
    print(myname(), "OK")


def test_runLongTimer():
    a = stages2beer.s2b.s2b(timerCtrl(), multiTimerDict())
    a.start()
    assert a.isAlive()
    a.join()
    assert not a.isAlive()
    print(myname(), "OK")


def test_runStop():
    a = stages2beer.s2b.s2b(simpleCtrl(), simpleDict())
    a.start()
    assert a.isAlive()
    a.stop()
    time.sleep(2)
    assert not a.isAlive()
    print(myname(), "OK")


def test_runPause():
    a = stages2beer.s2b.s2b(timerCtrl(), timerDict())
    a.start()
    assert a.isAlive()
    a.pause()
    time.sleep(2)
    assert a.isAlive()
    a.unpause()
    a.join()
    assert not a.isAlive()
    print(myname(), "OK")


def test_runSkip():
    a = stages2beer.s2b.s2b(simpleCtrl(), simpleDict())
    a.start()
    assert a.isAlive()
    a.skip()
    a.join()
    assert not a.isAlive()
    print(myname(), "OK")


def test_checkStage():
    a = stages2beer.s2b.s2b(timerCtrl(), timerDict())
    assert a.getStage() is None
    a.start()
    time.sleep(0.1)
    a.pause()
    assert a.getStage() == "1 stage"
    a.unpause()
    a.join()
    assert not a.isAlive()
    print(myname(), "OK")


if __name__ == "__main__":

    test_instantiate()
    test_controllerInstantiate()
    test_simpleStages()
    test_basicThread()
    test_ThreadEdgeCases()
    test_quickRun()
    test_check()
    test_getStages()
    test_runShortTimer()
    test_runLongTimer()
    test_runStop()
    test_runPause()
    test_runSkip()
    test_checkStage()
    print("====SUCCESS====")
