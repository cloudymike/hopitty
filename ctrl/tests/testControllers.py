import time
import genctrl
import hoptimer
import hotWaterTun
import pump
import controllers


def createCtrl():
    """Instantiate a list of all controllers"""
    ctrl = controllers.controllers()
    ctrl.addController(genctrl.genctrl())
    ctrl.addController(hoptimer.hoptimer_sim())
    ctrl.addController(pump.hwPump_sim())
    ctrl.addController(hotWaterTun.hwtsim(None))
    return(ctrl)


def testShutdown():
    ctrl=createCtrl()
    assert len(ctrl) > 0
    ctrl.shutdown()
    assert len(ctrl) == 0

def testStatus():
    ctrl=createCtrl()
    assert len(ctrl) > 0
    status = ctrl.status()
    assert len(status) > 0

def testStartStop():
    ctrl = createCtrl()
    ctrl.stop()
    settings = {}
    for key, c in ctrl.items():
        assert not c.isActive()
        s = {}
        s['targetValue'] = 1
        s['active'] = True
        settings[key] = s
    print settings
    ctrl.run(settings)
    for key, c in ctrl.items():
        assert c.isActive()



