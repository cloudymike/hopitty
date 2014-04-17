import json
import threading
import stages2beer
import ctrl
import appliances
import recipeReader
import inspect
import time
import dataMemcache as datastore


def printMyName():
    myname = inspect.stack()[1][3]
    if threading.activeCount() != 1:
        print threading.activeCount()
        print threading.enumerate()
        print myname, "did not cleanup threads"
        assert False
    print "....................", myname


def resetData(data):
    """
    Make sure that the datastore is reset to reasonable values
    """
    data.setTerminate(False)
    data.setCtrlRunning(False)
    data.setSkip(False)
    data.setPause(False)


def timerCtrl():
    """Instantiate a list of several controllers"""
    ctrl1 = ctrl.controllerList()
    ctrl1.addController('timer', appliances.hoptimer())
    return(ctrl1)


def timerDict():
    return({"1 stage": {"timer": {"active": True, "targetValue": 3}}})


def test_instantiate():
    """
    Trivial test, just check that the class is OK
    Start a loop and expect it to finish
    """
    bl = stages2beer.brewloop()
    assert not bl.isAlive()
    printMyName()


def test_stop():
    """
    Test that stop method and stopflag event works
    """
    bl = stages2beer.brewloop()
    bl.start()
    bl.stop()
    bl.join(5)
    assert not bl.isAlive()
    printMyName()


def test_terminate():
    """
    Test that data communication work, stop with data set
    """
    md = datastore.brewData()
    md.setTerminate(False)
    bl = stages2beer.brewloop()
    bl.start()
    md.setTerminate(True)
    bl.join(5)
    assert not bl.isAlive()
    printMyName()


def test_runTimer():
    """
    Run a program with a one step simple timer
    """
    md = datastore.brewData()
    md.setTerminate(False)
    bl = stages2beer.brewloop(timerCtrl())
    bl.start()
    md.setCurrentRecipe(timerDict())
    md.setCtrlRunning(True)
    time.sleep(0.5)
    assert md.getCurrentStage() == '1 stage'
    bl.stop()
    bl.join()
    assert not bl.isAlive()
    printMyName()


def test_runFast():
    """
    Run a program quickly and check that it stops
    """
    s = {"1 stage": {"timer": {"active": True, "targetValue": 0.0001}}}
    md = datastore.brewData()
    resetData(md)
    bl = stages2beer.brewloop(timerCtrl())
    bl.start()
    md.setCurrentRecipe(s)
    md.setCtrlRunning(True)
    time.sleep(3)
    assert not md.getCtrlRunning()
    assert md.getCurrentStage() != '1 stage'
    bl.stop()
    bl.join()
    assert not bl.isAlive()
    printMyName()


def test_runSkip():
    """
    Test skipping
    """
    s = {"1 stage": {"timer": {"active": True, "targetValue": 1}},
         "2 stage": {"timer": {"active": True, "targetValue": 1}}}
    md = datastore.brewData()
    resetData(md)
    bl = stages2beer.brewloop(timerCtrl())
    bl.start()
    md.setCurrentRecipe(s)
    md.setCtrlRunning(True)
    time.sleep(1)
    assert md.getCurrentStage() == '1 stage'
    md.setSkip(True)
    time.sleep(1)
    assert md.getCurrentStage() == '2 stage'
    md.setCtrlRunning(False)
    bl.stop()
    bl.join()
    assert not bl.isAlive()
    printMyName()


if __name__ == "__main__":
    print threading.activeCount()
    test_stop()
    print threading.activeCount()
    print threading.enumerate()
    test_instantiate()
    test_runSkip()
    test_runFast()
    test_runTimer()
    test_terminate()
    print "====SUCCESS===="
