# Basic smoke tests to make sure that
# things are not messed up as code is added

import appliances.hotWaterTun


def testPass():
    pass


def testHwtOnOff():
    mytun = appliances.hotWaterTun.hwt()
    status = mytun.status()
    assert status == 'Off'
    mytun.on()
    status = mytun.status()
    assert status == 'On'
    mytun.off()
    status = mytun.status()
    assert status == 'Off'


def testHwtThermostat():
    mytun = appliances.hotWaterTun.hwt()
    status = mytun.status()
    assert status == 'Off'
    T = mytun.get()
    mytun.set(T + 5)
    mytun.update()
    status = mytun.status()
    assert status == 'On'
