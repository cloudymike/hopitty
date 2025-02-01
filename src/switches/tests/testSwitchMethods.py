import mySwitchLoader


def test_load():
    """
    Check that the loader works
    """
    s = mySwitchLoader.mySwitchLoader()
    s.build()
    s.list()
    instances = s.instances()
    assert len(instances) > 0


def test_error():
    """
    Check that the errors can be checked and reset on
    each sensor
    """
    allS = mySwitchLoader.mySwitchLoader()
    allS.build()
    for sname, sobj in allS.instances().iteritems():
        assert not sobj.hasError()
        sobj.forceError()
        assert sobj.hasError()
        sobj.clearError()
        assert not sobj.hasError()


def test_on():
    """
    Check that the errors can be checked and reset on
    each sensor
    """
    allS = mySwitchLoader.mySwitchLoader()
    allS.build()
    for sname, sobj in allS.instances().iteritems():
        sobj.on()
        sobj.off()
        assert not sobj.hasError()


def test_HWOK():
    """
    Check that the errors can be checked and reset on
    each sensor
    """
    allS = mySwitchLoader.mySwitchLoader()
    allS.build()
    for sname, sobj in allS.instances().iteritems():
        print(sname, sobj.HWOK())
        assert not sobj.HWOK()


if __name__ == "__main__":
    test_load()
    test_error()
    test_HWOK()
    test_on()

    print("=====SUCCESS=====")
