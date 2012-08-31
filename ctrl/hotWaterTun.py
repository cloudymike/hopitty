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
        self.setTemp=70

    def temperature(self):
        return(self.currTemp)

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def setTemp(self,temperature):
        self.setTemp=temperature

    def thermostat(self):
        if self.powerOn:
            self.currTemp = self.currTemp+1
        else:
            self.currTemp = self.currTemp-1

    def on(self):
        self.powerOn = True

    def off(self):
        self.powerOn = False

class hwtsim(hwt):

    def thermostat(self):
        if self.powerOn:
            self.currTemp = self.currTemp+3
        else:
            self.currTemp = self.currTemp-1

class hwtHW(hwt):
    def __init__(self):
        print "Initializing hardware"
        
#        logger = logging.getLogger()
#        hdlr = logging.StreamHandler() # Console
#        formatter = logging.Formatter('%(module)s - %(asctime)s %(levelname)s %(message)s')
#        hdlr.setFormatter(formatter)
#        logger.addHandler(hdlr) 
#        logger.setLevel(logging.DEBUG)

        if False:
            self.dev = CM11('/dev/ttyUSB0')
            dev.open()
            self.hotWaterTun = dev.actuator("H14")
            status = 'Off'

    def temperature(self):
        return subprocess.check_output('./mytemp')


    def on(self):
        self.hotWaterTun.on()
    def off(self):
        self.hotWaterTun.off()

