
import time
import ctrl.genctrl
import ctrl.hoptimer
import ctrl.hotWaterTun
import ctrl.hwPump

def createList():
    """Instantiate a list of all controllers"""
    ctrlList = []
    ctrlList.append(ctrl.genctrl.genctrl())
    ctrlList.append(ctrl.hoptimer.hoptimer_sim())
    ctrlList.append(ctrl.hwPump.hwPump())
    ctrlList.append(ctrl.hotWaterTun.hwtsim(None))
    return(ctrlList)

def testInitialValues():
    """Instantiate all ctrls and run loop tests
    Initial value check"""
    ctrlList=createList()
    assert len(ctrlList) > 0
    for ctrl in ctrlList:
        print ctrl.__class__.__name__
        assert ctrl.isActive() == False

def testRunNotComplete():
    """Instantiate all ctrls and run loop tests
    Start and check values"""
    ctrlList=createList()
    assert len(ctrlList) > 0
    for ctrl in ctrlList:
        ctrl.set(5)
        ctrl.start()
        print ctrl.__class__.__name__
        assert ctrl.targetMet() == False
        assert ctrl.isActive() == True


def testStartStop():
    """Instantiate all ctrls and run loop tests
    Start and check values"""
    ctrlList=createList()
    assert len(ctrlList) > 0
    for ctrl in ctrlList:
        ctrl.set(5)
        ctrl.start()
        assert ctrl.isActive() == True
        ctrl.stop()
        assert ctrl.isActive() == False
        ctrl.start()
        assert ctrl.isActive() == True

def testRunChanges():
    """Instantiate all ctrls and run loop tests
    Start and check values"""
    ctrlList=createList()
    assert len(ctrlList) > 0
    valuelist=[]
    for ctrl in ctrlList:
        ctrl.set(5)
        ctrl.start()
        valuelist.append(ctrl.get())
        assert ctrl.targetMet() == False
        assert ctrl.isActive() == True
    time.sleep(1)
    i = iter(valuelist)
    for ctrl in ctrlList:
        a=ctrl.get()
        b=i.next()
        print a,b
        assert a != b

