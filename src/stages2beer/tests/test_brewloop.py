import json
import threading
import stages2beer
import ctrl
import appliances
import recipeReader
import inspect
import time
import dataMemcache as datastore
import sys
import recipelistmgr
import xml.dom.minidom
import types


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


def recipeDict():
    rl = {}
    rl['1timer'] = timerDict()
    rl['2Fast'] = \
        {"1 stage": {"timer": {"active": True, "targetValue": 0.0001}}}
    rl['3skip'] = \
        {"1 stage": {"timer": {"active": True, "targetValue": 1}},
         "2 stage": {"timer": {"active": True, "targetValue": 1}}}
    rl['4pause'] = \
        {"1 stage": {"timer": {"active": True, "targetValue": 0.1}},
         "2 stage": {"timer": {"active": True, "targetValue": 1}}}
    return(rl)


def simpleBsmx():
    retval = """
<Cloud>
 <Name>Cloud</Name>
 <Data>
  <Cloud>
   <F_R_NAME>18 Rune Stone  IPA 2.5G</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Cloud>
  <Cloud>
   <F_R_NAME>19 Great Brew</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Cloud>
 </Data>
</Cloud>
    """
    return(retval)


def getSimpleBSMX():
    """ Get recipe from simpleBSMX, and return a recipe list"""
    rl = recipelistmgr.recipeListClass()
    doc = xml.dom.minidom.parseString(simpleBsmx())
    rl.readBMXdoc(doc)
    rl.printNameList()
    return(rl)


class simpleRecipeClass():

    def __init__(self):
        self.list = recipeDict()

    def getRecipe(self, name):
        return(self.list[name])


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
    md = datastore.brewData()
    md.setTerminate(False)
    bl = stages2beer.brewloop(timerCtrl(), simpleRecipeClass())
    bl.start()
    md.setSelectedRecipe('1timer')
    md.setCtrlRunning(True)
    time.sleep(0.5)
    assert bl.isAlive()
    bl.stop()
    bl.join(5)
    assert not bl.isAlive()
    printMyName()


def test_terminate():
    """
    Test that data communication work, stop with data set
    """
    md = datastore.brewData()
    resetData(md)
    md.setTerminate(False)
    bl = stages2beer.brewloop()
    bl.start()
    assert bl.isAlive()
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

    bl = stages2beer.brewloop(timerCtrl(), simpleRecipeClass())
    bl.start()

    md.setSelectedRecipe('1timer')

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
    #s = {"1 stage": {"timer": {"active": True, "targetValue": 0.0001}}}
    md = datastore.brewData()
    resetData(md)
    bl = stages2beer.brewloop(timerCtrl(), simpleRecipeClass())
    bl.start()
    md.setSelectedRecipe('2Fast')
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
    md = datastore.brewData()
    resetData(md)
    bl = stages2beer.brewloop(timerCtrl(), simpleRecipeClass())
    bl.start()
    md.setSelectedRecipe('3skip')
    md.setCtrlRunning(True)
    time.sleep(1)
    assert md.getCurrentStage() == '1 stage'
    md.setSkip(True)
    time.sleep(1)
    print md.getCurrentStage()
    assert md.getCurrentStage() == '2 stage'
    md.setCtrlRunning(False)
    bl.stop()
    bl.join()
    assert not bl.isAlive()
    printMyName()


def test_runPause():
    """
    Test Pause
    """
    md = datastore.brewData()
    resetData(md)
    bl = stages2beer.brewloop(timerCtrl(), simpleRecipeClass())
    bl.start()
    md.setSelectedRecipe('4pause')
    md.setCtrlRunning(True)
    md.setPause(True)
    time.sleep(2)
    assert md.getCurrentStage() == '1 stage'
    time.sleep(6)
    assert md.getCurrentStage() == '1 stage'
    md.setPause(False)

    md.setCtrlRunning(False)
    bl.stop()
    bl.join()
    assert not bl.isAlive()
    printMyName()


def test_threadUpAndDown():
    """
    Test that reassign of name works
    """
    md = datastore.brewData()
    resetData(md)
    md.setSelectedRecipe('1timer')
    a = stages2beer.s2b(timerCtrl(), simpleRecipeClass())
    a.start()
    a.stop()
    a.join()
    assert not a.isAlive()
    a = stages2beer.s2b()
    printMyName()


def test_testData():
    """
    Somewhat redundant, tests that the test data is OK
    Runs a test with recipe class and then the same test
    with the simpleRecipeClass and makes sure that the data
    is the same for the purpose of this test harness
    """
    rl = simpleRecipeClass()
    r = rl.getRecipe('1timer')
    assert isinstance(rl, types.InstanceType)
    for name, recipe in rl.list.items():
        assert isinstance(recipe, types.DictType)

    r2 = getSimpleBSMX()
    assert isinstance(rl, types.InstanceType)
    for name, recipe in r2.list.items():
        assert isinstance(recipe, types.InstanceType)
    printMyName()


def checkOnRecipe(rl):
    assert isinstance(rl, types.InstanceType)
    for name, recipe in rl.list.items():
        assert ((isinstance(recipe, types.DictType)) or
                (isinstance(recipe, types.InstanceType)))
        if isinstance(recipe, types.InstanceType):
            bsxml = recipe.getBSMXdoc()
            assert isinstance(bsxml, types.InstanceType)


def test_testMoreData():
    r1 = simpleRecipeClass()
    checkOnRecipe(r1)
    r2 = getSimpleBSMX()
    checkOnRecipe(r2)
    printMyName()


def test_badRecipeData():
    """
    Test that stop method and stopflag event works
    """
    md = datastore.brewData()
    md.setTerminate(False)
    bl = stages2beer.brewloop(timerCtrl(), simpleRecipeClass())
    bl.start()
    md.setSelectedRecipe('bogus')
    md.setCtrlRunning(True)
    time.sleep(0.5)
    assert bl.isAlive()
    bl.stop()
    bl.join(5)
    assert not bl.isAlive()
    printMyName()


if __name__ == "__main__":
    test_threadUpAndDown()
    test_badRecipeData()
    test_stop()

    test_runTimer()

    test_testData()
    test_testMoreData()

    test_runFast()
    test_runSkip()
    test_runPause()

    test_terminate()
    #print threading.activeCount()
    #print threading.activeCount()
    #print threading.enumerate()
    test_instantiate()

    assert threading.activeCount() == 1
    print "====SUCCESS===="
