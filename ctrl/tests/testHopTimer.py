# Basic smoke tests to make sure that
# things are not messed up as code is added

import hoptimer
import time

def testPass():
    pass

def testSetGetTime():
    m=hoptimer.hoptimer()
    m.set(5)
    assert m.get() == 5   

def testwaitamin():
    m=hoptimer.hoptimer()
    m.set(5)
    time.sleep(60)
    assert m.get() == 4   

