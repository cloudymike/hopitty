'''
Created on Nov 20, 2013

@author: mikael
'''
# import subprocess
import appliances.genctrl
import sensors


class mashStirrer(appliances.genctrl):
    """
    Manage the mash stirrer
    """
    def __init__(self):
        self.switch = None
        self.powerOn = False
        self.active = False
        self.target = 80
        self.unit = 'F'
        # self.sensor = sensors.tempermashStirrerSensor()
        # Set a generic sensor, later swap for same sensor as boiler.
        self.sensor = sensors.genericSensor()

    def __del__(self):
        self.powerOn = False
        print 'Powering down'

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def targetMet(self):
        return(True)

    def measure(self):
        self.actual = 0

    def stop(self):
        self.active = False
        self.off()

    def on(self):
        if self.switch != None:
            self.switch.on()
        self.powerOn = True

    def off(self):
        if self.switch != None:
            self.switch.off()
        self.powerOn = False

    def HWOK(self):
        if self.switch == None:
            return(False)
        if not self.switch.HWOK():
            return(False)
        return(self.sensor.HWOK())

if __name__ == '__main__':
    testmashStirrer = mashStirrer()
    testmashStirrer.on()
    while not testmashStirrer.targetMet():
        print testmashStirrer.get()
    for x in range(0, 15):
        print testmashStirrer.get()
