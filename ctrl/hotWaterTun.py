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
        self.currTemp = 50.0
        self.presetTemp = 999.99
        self.active = False
        self.unit = 'F'

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

    def set(self, preset):
        self.presetTemp = float(preset)

    def update(self):
        if self.targetMet():
            self.off()
        else:
            self.on()

    def targetMet(self):
        if self.currTemp < self.presetTemp:
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
            self.currTemp = self.currTemp + 1.0
        else:
            self.currTemp = self.currTemp - 1.0
        return(self.currTemp)


class hwtHW(hwt):
    def __init__(self, switch):
        self.hotWaterTun = switch
        self.powerOn = False
        self.hotWaterTun.off()
        self.active = False
        self.presetTemp = 70.0
        self.unit = 'F'
        self.currTemp = 70.0

    def measure(self):
        currTempStr = subprocess.check_output('../GoIO-2.28.0/mytemp/mytemp')
        try:
            self.currTemp = float(currTempStr)
        except:
            self.currTemp = 999.99
        return self.currTemp

    def on(self):
        self.hotWaterTun.on()
        self.powerOn = True

    def off(self):
        self.hotWaterTun.off()
        self.powerOn = False
