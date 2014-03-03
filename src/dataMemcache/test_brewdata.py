'''
Created on Mar 19, 2013

@author: mikael
'''

import time
from brewdata import brewData


def testControllersStatus():
    bd = brewData()
    empty = {}
    oneitem = {'a': 1}
    bd.setControllersStatus(oneitem)
    assert bd.getControllersStatus() == oneitem
    bd.setControllersStatus(empty)
    assert bd.getControllersStatus() == empty
    bd.setControllersStatus(None)
    assert bd.getControllersStatus() == empty


def testStagesList():
    bd = brewData()
    empty = {}
    oneitem = {'a': 1}
    bd.setStagesList(oneitem)
    assert bd.getStagesList() == oneitem
    bd.setStagesList(empty)
    assert bd.getStagesList() == empty
    bd.setStagesList(None)
    assert bd.getStagesList() == empty


def test_stage():
    bd = brewData()
    bd.setCtrlRunning(True)
    stage = 'DummyStage'
    bd.setCurrentStage(stage)
    assert stage == bd.getCurrentStage()
    bd.setCtrlRunning(False)
    assert "" == bd.getCurrentStage()


def testWatchdog():
    print "testWatchdog will take > 10s"
    bd = brewData()
    bd.resetWatchdog()
    assert not bd.checkWatchdog()
    time.sleep(11)
    assert bd.checkWatchdog()


def test_CtrlRunning():
    bd = brewData()
    bd.setCtrlRunning(True)
    assert bd.getCtrlRunning()
    bd.setCtrlRunning(False)
    assert not bd.getCtrlRunning()


def dummyRecipe(bd):
    bd.clearRecipe()
    bd.addToRecipe('Cascade', 1, 'dispenser1')
    bd.addToRecipe('Chocolate Malt', 8, 'mashtun')
    bd.addToRecipe('Pale Malt', 88, 'mashtun')
    return(bd.getRecipe())


def testRecipe():
    d1 = brewData()
    d2 = brewData()
    r0 = dummyRecipe(d1)
    r1 = d1.getRecipe()
    print r0
    print r1
    assert r0 == r1
    r2 = d2.getRecipe()
    print r2
    assert r0 == r2
    d2.addToRecipe('Crystal 40L', 4, 'mashtun')
    r1 = d1.getRecipe()
    r2 = d2.getRecipe()
    print r2
    assert len(r2) == len(r0) + 1
    assert r1 == r2
    assert r0 != r2

    c = d1.getRecipeContainers()
    print c
    assert len(c) > 0
    assert 'mashtun' in c
    if len(c) > 1:
        assert c[0] < c[1]

    mt = d1.getItemsInContainer('mashtun')
    print mt
    assert len(mt) > 0
    assert len(mt) < len(d1.getRecipe())
    print "testRecipe OK"


def testRecipeList():
    bd = brewData()
    empty = []
    oneitem = ['a']
    bd.setRecipeList(oneitem)
    assert bd.getRecipeList() == oneitem
    bd.setRecipeList(empty)
    assert bd.getRecipeList() == empty
    bd.setRecipeList(None)
    assert bd.getRecipeList() == empty


def testErrors():
    d1 = brewData()
    d1.unsetError()
    assert not d1.getError()
    d1.setError()
    assert d1.getError()
    d1.unsetError()
    assert not d1.getError()
    d1.setHWerror(errorText='Just testing')
    assert not d1.getError()
    d1.setHWerror(errorText='Just testing')
    d1.setHWerror(errorText='Just testing')
    d1.setHWerror(errorText='Just testing')
    d1.setHWerror(errorText='Just testing')
    d1.setHWerror(errorText='Just testing')
    assert d1.getError()
    d1.unsetError()
    d1.unsetHWerror()
    assert not d1.getError()

    print "testErrors OK"

#def testFail():
#    assert False

if __name__ == "__main__":
    test_stage()
    testRecipe()
    testErrors()
    testWatchdog()
    test_CtrlRunning()
