import pyb
import time
import json
from ds18x20 import DS18X20

gnd = pyb.Pin('Y11', pyb.Pin.OUT_PP)
gnd.low()
vcc = pyb.Pin('Y9', pyb.Pin.OUT_PP)
vcc.high()
d = DS18X20(pyb.Pin('Y10'))

led1 = pyb.LED(1)
led2 = pyb.LED(2)
led3 = pyb.LED(3)
led4 = pyb.LED(4)

LEDS = [led1, led2, led3, led4]
mp=pyb.USB_VCP()
i=0
accel = pyb.Accel()

while(1):
    for l in LEDS:
        l.on()
        mydict = {}
        mydict['message'] = 'jsontesting'
        mydict['count'] = i
        mydict['x'] = accel.x()
        mydict['y'] = accel.y()
        mydict['temperature'] = d.read_temp()
        mystr = json.dumps(mydict)
        mp.write(mystr)
        mp.write('\n')

        i=i+1
        time.sleep(0.1)
        l.off()


