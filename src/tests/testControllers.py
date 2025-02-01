import appliances.boiler
import appliances.hoptimer
#import appliances.hotWaterTun
import appliances.hwPump
import ctrl.controllers
import appliances.circulationPump


def createCtrl():
    """Instantiate a list of all controllers"""

    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.addController('genctrl', appliances.genctrl.genctrl())
    ctrl1.addController('timer', appliances.hoptimer.hoptimer())
    ctrl1.addController('pump', appliances.hwPump.hwPump())
    ctrl1.addController('circulationPump', appliances.circulationPump.circulationPump())
    ctrl1.addController('heater', appliances.hotWaterTun.hwt())
    ctrl1.addController('boiler', appliances.boiler.boiler())
    return(ctrl1)


def testss1():
    ctrl1 = createCtrl()
    assert len(ctrl1) > 0
    ctrl1.shutdown()
    assert len(ctrl1) == 0


def testss2():
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    assert len(ctrl1) > 0
    ctrl1.shutdown()
    assert len(ctrl1) == 0


def testStatus():
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    assert len(ctrl1) > 0
    status = ctrl1.status()
    assert len(status) > 0


def testStartStop():
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
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


def testTarget():
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    for key, c in ctrl1.items():
        testVal = 3.1415926
        c.set(testVal)
        chkVal = c.getTarget()
        print testVal, key, chkVal
        assert testVal == chkVal


def testTargetMet():
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    for key, c in ctrl1.items():
        curVal = c.get()
        curTarget = c.getTarget()
        if curTarget:
            if curVal > curTarget:
                c.set(curVal + 10)
            else:
                c.set(curVal - 10)
        else:
            if curVal < curTarget:
                c.set(curVal - 10)
            else:
                c.set(curVal + 10)
        assert curTarget != c.getTarget()


def testUnit():
    """
    Test that unit is a string
    """
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    for key, c in ctrl1.items():
        s = c.getUnit()
        assert isinstance(s, str) or (s is None)
        if s is not None:
            assert len(s) > 0


def testHWOK():
    """
    Test that HWOK is a boolean
    More importantly, test that HWOK is implemented and does not crash
    """
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    for key, c in ctrl1.items():
        s = c.HWOK()
        print key, s
        assert isinstance(s, bool)


def testVal():
    """
    Test that current value and target value is a number
    """
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    for key, c in ctrl1.items():
        a = c.get()
        t = c.getTarget()
        assert isinstance(a, int) or isinstance(a, float)
        assert isinstance(t, int) or isinstance(t, float)


def testPowerOn():
    """
    Test that power is off after stop, and it is a boolean
    """
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    for key, c in ctrl1.items():
        print key
        c.stop()
        assert not c.getPowerOn()


def testError():
    """
    Test that power is off after stop, and it is a boolean
    """
    ctrl1 = ctrl.controllers.controllerList()
    ctrl1.load()
    for key, c in ctrl1.items():
        print key
        assert not c.hasError()
        c.forceError()
        assert c.hasError()
        c.clearError()
        assert not c.hasError()


if __name__ == '__main__':
    testError()
    testHWOK()
