# Basic smoke tests to make sure that
# things are not messed up as code is added

import ctrl.hoptimer
import time

def testPass():
    pass

def testSetGetTime():
    m=ctrl.hoptimer.hoptimer()
    m.set(5)
    assert m.get() == 0   
    assert m.targetMet() == False

def testwaitamin():
    m=ctrl.hoptimer.hoptimer()
    m.set(0.01)
    m.start()
    time.sleep(1)
    assert m.get() > 0 
    assert m.targetMet() == True  
   
def testStop():
    m=ctrl.hoptimer.hoptimer()
    m.set(1)
    time.sleep(1)
    m.stop()
    assert m.get() == 0

