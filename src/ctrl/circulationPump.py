#!/usr/bin/python

import time
import genctrl


class circulationPump(genctrl.genctrl):
    """
    The circulation pump is just controller by explicit on and off
    The target is always met
    The circulation pump will not change status on update
    """

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

    def measure(self):
        self.actual = 0
        
    def targetMet(self):
        return(True)

    def update(self):
        pass
 
    def pumpOn(self):
        self.powerOn = True
        self.pumpMotor.on()

    def pumpOff(self):
        """ Pump on regardless of target"""
        self.powerOn = False
        self.pumpMotor.off()

    def stop(self):
        self.target = 0
        self.actual = 0
        self.active = False
        self.pumpOff()

    def start(self):
        self.active = True
        self.pumpOn()