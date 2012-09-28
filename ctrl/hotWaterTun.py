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
import genctrl

class hwt(genctrl.genctrl):
    def __init__(self):
        self.powerOn = False
        self.currTemp = 70
        self.presetTemp = 70
        self.active=False

    def __del__(self):
        self.powerOn = False
        print 'Powering down'

    def temperature(self):
        return(self.currTemp)

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def setTemp(self, preset):
        self.presetTemp = preset

    def update(self):
        if self.temperature() < self.presetTemp:
            self.on()
        else:
            self.off()

    def targetMet(self):
        if self.temperature() < self.presetTemp:
            return(False)
        else:
            return(True)

    def get(self):
        return(self.temperature())

    def on(self):
        self.powerOn = True

    def off(self):
        self.powerOn = False

    def stop(self):
        self.active = False
        self.off()


class hwtsim(hwt):

    def temperature(self):
        if self.powerOn:
            self.currTemp = self.currTemp + 2
        else:
            self.currTemp = self.currTemp - 1
        return(self.currTemp)


class hwtHW(hwt):
    def __init__(self):
        print "Initializing hardware"

        if True:
            self.dev = CM11('/dev/ttyUSB0')
            self.dev.open()
            self.hotWaterTun = self.dev.actuator("H14")
            self.powerOn = False
            self.hotWaterTun.off()
            self.active=False

    def temperature(self):
        currTempStr = subprocess.check_output('./mytemp')
        try:
            currTemp = int(currTempStr)
        except:
            currTemp = 999
        return currTemp

    def on(self):
        self.hotWaterTun.on()
        self.powerOn = True

    def off(self):
        self.hotWaterTun.off()
        self.powerOff = False
