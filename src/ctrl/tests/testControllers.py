import ctrl.genctrl
import ctrl.hoptimer
import ctrl.hotWaterTun
import ctrl.hwPump
import ctrl.controllers
import ctrl.circulationPump
import ctrl.simswitch
import ctrl.boiler

def createCtrl():
    """Instantiate a list of all controllers"""
    cirsw = ctrl.simswitch.simSwitch()
    pumpsw = ctrl.simswitch.simSwitch()

    ctrl1 = ctrl.controllers()
    ctrl1.addController('genctrl', ctrl.genctrl.genctrl())
    ctrl1.addController('timer', ctrl.hoptimer.hoptimer())
    ctrl1.addController('pump', ctrl.hwPump.hwPump(pumpsw))
    ctrl1.addController('circulationPump', ctrl.circulationPump.circulationPump(cirsw))
    ctrl1.addController('heater', ctrl.hotWaterTun.hwtsim())
    ctrl1.addController('boiler', ctrl.boiler.boiler())
    return(ctrl1)


def testss():
    ctrl1=createCtrl()
    assert len(ctrl1) > 0
    ctrl1.shutdown()
    assert len(ctrl1) == 0

def testStatus():
    ctrl1=createCtrl()
    assert len(ctrl1) > 0
    status = ctrl1.status()
    assert len(status) > 0

def testStartStop():
    ctrl1 = createCtrl()
    ctrl1.stop()
    settings = {}
    for key, c in ctrl1.items():
        assert not c.isActive()
        s = {}
        s['targetValue'] = 1
        s['active'] = True
        settings[key] = s
    print settings
    ctrl1.run(settings)
    for key, c in ctrl1.items():
        assert c.isActive()



