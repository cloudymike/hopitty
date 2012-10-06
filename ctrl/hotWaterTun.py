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
        self.currTemp = 0
        self.presetTemp = 999.99
        self.active = False
        self.unit = 'F'
        print "hwt setup ", self.presetTemp

    def __del__(self):
        self.powerOn = False
        print 'Powering down'

    def measure(self):
        return(self.currTemp)

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def setTemp(self, preset):
        self.presetTemp = preset
        print "Setting to ", self.presetTemp

    def set(self, preset):
        self.setTemp(preset)

    def update(self):
        if self.targetMet():
            self.off()
        else:
            self.on()

    def targetMet(self):
        print self.measure(), self.presetTemp
        if self.measure() < self.getTarget():
            return(False)
        else:
            return(True)

    def get(self):
        return(self.measure())

    def getTarget(self):
        return(self.presetTemp)

    def on(self):
        self.powerOn = True

    def off(self):
        self.powerOn = False

    def stop(self):
        self.active = False
        self.off()


class hwtsim(hwt):

    def measure(self):
        if self.powerOn:
            self.currTemp = self.currTemp + 1
        else:
            self.currTemp = self.currTemp - 1
        return(self.currTemp)


class hwtHW(hwt):
    def __init__(self, switch):
        self.hotWaterTun = switch
        self.powerOn = False
        self.hotWaterTun.off()
        self.active = False
        self.presetTemp = 70
        self.unit = 'F'

    def measure(self):
        currTempStr = subprocess.check_output('../GoIO-2.28.0/mytemp/mytemp')
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
