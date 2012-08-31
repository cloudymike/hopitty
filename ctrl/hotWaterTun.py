#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess
import getopt
import sys
from x10.controllers.cm11 import CM11


class hwt:
    def __init__(self):
        self.powerOn=False
        self.currTemp=70
        self.presetTemp=70

    def __del__(self):
        self.powerOn=False
        print 'Powering down'

    def temperature(self):
        return(self.currTemp)

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def setTemp(self,preset):
        self.presetTemp=preset

    def thermostat(self):
        if self.temperature() < self.presetTemp:
            self.on()
        else:
            self.off()

    def on(self):
        self.powerOn = True

    def off(self):
        self.powerOn = False

class hwtsim(hwt):

    def temperature(self):
        if self.powerOn:
            self.currTemp = self.currTemp+2
        else:
            self.currTemp = self.currTemp-1
        return(self.currTemp)


class hwtHW(hwt):
    def __init__(self):
        print "Initializing hardware"
        self.powerOn=False
        
#        logger = logging.getLogger()
#        hdlr = logging.StreamHandler() # Console
#        formatter = logging.Formatter('%(module)s - %(asctime)s %(levelname)s %(message)s')
#        hdlr.setFormatter(formatter)
#        logger.addHandler(hdlr) 
#        logger.setLevel(logging.DEBUG)

        if True:
            self.dev = CM11('/dev/ttyUSB0')
            self.dev.open()
            self.hotWaterTun = self.dev.actuator("H14")
            self.powerOn=False
            self.hotWaterTun.off()

    def temperature(self):
        currTempStr=subprocess.check_output('./mytemp')
        currTemp=int(currTempStr)
        return currTemp

    def on(self):
        self.hotWaterTun.on()
        self.powerOn = True
    def off(self):
        self.hotWaterTun.off()
        self.powerOff = False

