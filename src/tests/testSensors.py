import appliances
import ctrl


def testGenSensor():
    c1 = appliances.genctrl()
    assert isinstance(c1.sensor.getID(), str)
    assert (isinstance(c1.sensor.getValue(), int) or \
            isinstance(c1.sensor.getValue(), float))


def testSensors():
    clist = ctrl.controllerList()
    clist.load()
    for key, c1 in clist.items():
        print "Checking sensor", key
        assert isinstance(c1.sensor.getID(), str)
        assert (isinstance(c1.sensor.getValue(), int) or \
                isinstance(c1.sensor.getValue(), float))


if __name__ == "__main__":
    c1 = appliances.genctrl()
    print c1.sensor.getID()
    testGenSensor()
    testSensors()
    if isinstance(c1.sensor.getID(), str):
        print "ID OK"
    else:
        print "ID FAIL"
