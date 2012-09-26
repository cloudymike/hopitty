# Basic smoke tests to make sure that
# things are not messed up as code is added

import hoptimer
import time

def testPass():
    pass

def testSetGetTime():
    m=hoptimer.hoptimer()
    m.set(5)
    assert m.get() == 0   
    assert m.done() == False

def testwaitamin():
    m=hoptimer.hoptimersim()
    m.set(1)
    time.sleep(1)
    assert m.get() > 0 
    assert m.done() == True  
   
def testStop():
    m=hoptimer.hoptimersim()
    m.set(1)
    time.sleep(1)
    m.stop()
    assert m.get() == 0

