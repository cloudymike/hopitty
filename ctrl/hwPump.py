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

class hwPump(genctrl.genctrl):
    
    def __init__(self):
        self.actual=0.000
        self.target=0
        self.active=False
        self.totalVol = 0
        self.pumpRunning=False
        self.absSec=time.time()
        self.SEC_PER_QUART=41.0


    def measure(self):
        currSec=time.time()
        deltaSec=currSec-self.absSec
        deltavol=deltaSec/self.SEC_PER_QUART
        self.absminutes=currSec
        if self.pumpRunning:
            self.actual=self.actual+deltavol
            self.totalVol=self.actual+deltavol


    def update(self):
        self.measure()
        if self.targetMet():
            self.pumpOff()

    def pumpOn(self):
        self.pumpRunning=True

    def pumpOff(self):
        self.pumpRunning=False

    def stop(self):
        self.target = 0
        self.actual = 0
        self.active = False
        self.pumpOff()

    def start(self):
        self.active = True
        self.pumpOn()



