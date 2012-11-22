import appliances.boiler

import appliances.hoptimer
import appliances.hotWaterTun
import appliances.hwPump
import ctrl.controllers
import appliances.circulationPump
import ctrl.simswitch

def createCtrl():
    """Instantiate a list of all controllers"""
    cirsw = ctrl.simswitch.simSwitch()
    pumpsw = ctrl.simswitch.simSwitch()

    ctrl1 = ctrl.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl())
    ctrl1.addController('timer', appliances.hoptimer())
    ctrl1.addController('pump', appliances.hwPump())
    ctrl1.addController('circulationPump', appliances.circulationPump())
    ctrl1.addController('heater', appliances.hwtsim())
    ctrl1.addController('boiler', appliances.boiler())
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



