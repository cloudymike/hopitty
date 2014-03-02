# Testing the start and stop button
# Otpionally other control buttons should be added here.

import dataMemcache


def testStart():
    mydata = dataMemcache.brewData()

    mydata.setCtrlRunning(False)
    assert not mydata.getCtrlRunning()
    mydata.setCtrlRunning(True)
    assert mydata.getCtrlRunning()
    mydata.setCtrlRunning(False)
    assert not mydata.getCtrlRunning()
    print "OK"

if __name__ == "__main__":
    testStart()
