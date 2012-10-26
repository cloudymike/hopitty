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
import pumpUSB
from x10.controllers.cm11 import CM11


class circulationPump(genctrl.genctrl):

    def __init__(self):
        self.actual = 0.000
        self.target = 0
        self.active = False
        self.totalVol = 0
        self.powerOn = False
        self.absSec = time.time()
        self.SEC_PER_QUART = 41.0
        self.unit = 'Qt'

    def measure(self):
        currSec = time.time()
        deltaSec = currSec - self.absSec
        deltavol = deltaSec / self.SEC_PER_QUART
        self.absSec = currSec
        if self.powerOn:
            self.actual = self.actual + deltavol
            self.totalVol = self.actual + deltavol

    def update(self):
        self.measure()
        if self.targetMet():
            self.pumpOff()

    def pumpOn(self):
        if not self.targetMet():
            self.powerOn = True

    def pumpOff(self):
        self.powerOn = False

    def stop(self):
        self.target = 0
        self.actual = 0
        self.active = False
        self.pumpOff()

    def start(self):
        self.active = True
        self.pumpOn()




class circulationPump_sim(circulationPump):
    """
    The pump is just controller by explicit on and off
    The target is always met
    The pump will not change status on update
    """
    def __init__(self):
        self.actual = 0
        self.target = 0
        self.active = False
        self.totalVol = 0
        self.powerOn = False
        self.absSec = time.time()
        self.SEC_PER_QUART = 41.0
        self.unit = 'Qt'
        
    def measure(self):
        self.actual = 0
        
    def targetMet(self):
        return(True)
    
    def update(self):
        pass
    
    def pumpOn(self):
        """ Pump on regardless of target"""
        self.powerOn = True



class circulationPump_usb(circulationPump):
    def __init__(self, pumpUSBswitch):
        self.actual = 0.000
        self.target = 0
        self.active = False
        self.totalVol = 0
        self.powerOn = False
        self.absSec = time.time()
        self.SEC_PER_QUART = 39.0
        self.unit = 'Qt'
 
        self.pumpMotor = pumpUSBswitch
        self.pumpMotor.off()

    def pumpOn(self):
        self.powerOn = True
        self.pumpMotor.on()

    def pumpOff(self):
        """ Pump on regardless of target"""
        self.powerOn = False
        self.pumpMotor.off()
              
    def measure(self):
        self.actual = 0
        
    def targetMet(self):
        return(True)
    
    def update(self):
        pass
    

