import pyb
import time
import json

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

        mystr = json.dumps(mydict)
        mp.write(mystr)
        mp.write('\n')

        i=i+1
        time.sleep(0.1)
        l.off()


