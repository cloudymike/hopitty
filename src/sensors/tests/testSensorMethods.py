import mySensorLoader


def test_load():
    """
    Check that the loader works
    """
    s = mySensorLoader.mySensorLoader()
    s.build()
    s.list()
    instances = s.instances()
    assert len(instances) > 0


def test_error():
    """
    Check that the errors can be checked and reset on
    each sensor
    """
    allS = mySensorLoader.mySensorLoader()
    allS.build()
    for sname, sobj in allS.instances().items():
        assert not sobj.hasError()
        sobj.forceError()
        assert sobj.hasError()
        sobj.clearError()
        assert not sobj.hasError()


def test_ID():
    """
    Check that the errors can be checked and reset on
    each sensor
    """
    allS = mySensorLoader.mySensorLoader()
    allS.build()
    for sname, sobj in allS.instances().items():
        sobj.setID('qwerty')
        assert sobj.getID() == 'qwerty'


if __name__ == "__main__":
    test_load()
    test_error()
    test_ID()

    print("=====SUCCESS=====")
