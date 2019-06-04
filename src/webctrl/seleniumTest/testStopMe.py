# Test that non blocking start works
# This is a simple test that is superseded in other
# tests, but keep it to check that webserver
# can start and stop.

import webctrl
import time
import helpers


def testNonBlocking():
    #controllers = ctrl.setupControllers(False, True, True)
    p = helpers.findPort()
    server = helpers.MyWSGIRefServer(host="localhost", port=p)
    server.quiet = True
    print server.port
    brewme = webctrl.runbrew(
        helpers.timerCtrl(),
        helpers.getSimpleBSMX(),
        server)
    brewme.startNonBlocking()

    print "up and running"
    time.sleep(1)
    print "time to go"
    brewme.stop()


if __name__ == "__main__":
    testNonBlocking()
