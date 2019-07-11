import pyb
import time
import json
import ubinascii
from ds18x20 import DS18X20
from onewire import OneWire

led1 = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)
led4 = pyb.LED(4)
led1.on()
gnd = pyb.Pin('Y11', pyb.Pin.OUT_PP)
gnd.low()
vcc = pyb.Pin('Y9', pyb.Pin.OUT_PP)
vcc.high()
d = DS18X20(pyb.Pin('Y10'))
o = OneWire(pyb.Pin('Y10'))

mp=pyb.USB_VCP()

led1.off()

while(1):
    led4.on()
    mydict = {}
    # For backwards compatibility keep this one
    mydict['temperature'] = d.read_temp()
    devicelist = o.scan()
    tempdict = {}
    led4.off()
    for device in devicelist:
        tempdict[ubinascii.hexlify(device)] = d.read_temp(device)
    mydict['devicelist'] = tempdict
    mystr = json.dumps(mydict)
    mp.write(mystr)
    mp.write('\n')
    time.sleep(0.1)



