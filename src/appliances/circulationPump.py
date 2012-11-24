#!/usr/bin/python

import time
import appliances.genctrl


class circulationPump(appliances.genctrl):
    """
    The circulation pump is just controller by explicit on and off
    The target is always met
    The circulation pump will not change status on update
    """

    def __init__(self):
        self.actual = 0.000
        self.target = 0
        self.active = False
        self.totalVol = 0
        self.powerOn = False
        self.absSec = time.time()
        self.SEC_PER_QUART = 39.0
        self.unit = 'Qt'
        self.pumpMotor = None
        self.sensor = circulationPump.gensensor()

    def connectSwitch(self, switch):
        """
        If a switch is required, this will connect it with the devices
        The switch object needs to have a method on and a method off.
        """
        self.pumpMotor = switch

    def measure(self):
        self.actual = 0

    def targetMet(self):
        return(True)

    def update(self):
        pass

    def pumpOn(self):
        self.powerOn = True
        if self.pumpMotor != None:
            self.pumpMotor.on()

    def pumpOff(self):
        """ Pump on regardless of target"""
        self.powerOn = False
        if self.pumpMotor != None:
            self.pumpMotor.off()

    def stop(self):
        self.target = 0
        self.actual = 0
        self.active = False
        self.pumpOff()

    def start(self):
        self.active = True
        self.pumpOn()
