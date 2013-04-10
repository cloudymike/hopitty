# Testing the start and stop button
# Otpionally other control buttons should be added here.

import dataMemcache


def testStart():
    mydata = dataMemcache.brewData()

    mydata.setRunStatus('stop')
    assert mydata.getRunStatus() != 'run'
    mydata.setRunStatus('run')
    assert mydata.getRunStatus() == 'run'
    mydata.setRunStatus('stop')
    assert mydata.getRunStatus() != 'run'
    print "OK"

if __name__ == "__main__":
    testStart()
