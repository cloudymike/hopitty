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


if __name__ == "__main__":
    test_load()
    test_error()

    print "=====SUCCESS====="
