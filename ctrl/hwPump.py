#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess
import getopt
import sys
import genctrl
from x10.controllers.cm11 import CM11


class hwPump(genctrl.genctrl):
    
    def __init__(self):
        self.actual=0.000
        self.target=0
        self.active=False
        self.totalVol = 0
        self.powerOn=False
        self.absSec=time.time()
        self.SEC_PER_QUART=41.0
        self.unit='Qt'


    def measure(self):
        currSec=time.time()
        deltaSec=currSec-self.absSec
        deltavol=deltaSec/self.SEC_PER_QUART
        self.absSec=currSec
        if self.powerOn:
            self.actual=self.actual+deltavol
            self.totalVol=self.actual+deltavol


    def update(self):
        self.measure()
        if self.targetMet():
            self.pumpOff()

    def pumpOn(self):
        if not self.targetMet():
            self.powerOn=True

    def pumpOff(self):
        self.powerOn=False

    def stop(self):
        self.target = 0
        self.actual = 0
        self.active = False
        self.pumpOff()

    def start(self):
        self.active = True
        self.pumpOn()


class hwPump_sim(hwPump):
    pass


class hwPump_hw(hwPump):

    def __init__(self,switch):
        self.actual=0.000
        self.target=0
        self.active=False
        self.totalVol = 0
        self.powerOn=False
        self.absSec=time.time()
        self.SEC_PER_QUART=39.0
        self.unit='Qt'

        self.pumpMotor = switch
        self.pumpMotor.off()

    def pumpOn(self):
        if not self.targetMet():
            self.powerOn=True
            self.pumpMotor.on()
            print "Pump motor on"

    def pumpOff(self):
        self.powerOn=False
        self.pumpMotor.off()
        print "Pump motor off"




