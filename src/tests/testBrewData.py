import dataMemcache
import time


def testError():
    d = dataMemcache.brewData()
    e = dataMemcache.brewData()
    d.setPause(False)
    assert not d.getError()
    d.setError()
    time.sleep(1)
    assert d.getError()
    assert e.getError()
    assert d.getPause()
    assert e.getPause()
    d.unsetError()
    assert not d.getError()
    assert not e.getError()
    d.setPause(False)
    assert not d.getPause()
    assert not e.getError()
