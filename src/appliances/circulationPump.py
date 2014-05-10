#!/usr/bin/python

import time
import appliances.genctrl
import sensors


class circulationPump(appliances.genctrl):
    """
    The circulation pump is just controller by explicit on and off
    The target is always met
    The circulation pump will not change status on update
    """

    def __init__(self):
        self.errorState = False  # If an error has occured
        self.actual = 0.000
        self.target = 0
        self.active = False
        self.totalVol = 0
        self.powerOn = False
        self.absSec = time.time()
        self.SEC_PER_QUART = 39.0
        self.unit = None
        self.pumpMotor = None
        self.sensor = sensors.genericSensor()

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
        if self.powerOn:
            self.pumpOn()
        else:
            self.pumpOff()

    def pumpOn(self):
        self.powerOn = True
        if self.pumpMotor is not None:
            self.pumpMotor.on()

    def pumpOff(self):
        """ Pump on regardless of target"""
        self.powerOn = False
        if self.pumpMotor is not None:
            self.pumpMotor.off()

    def stop(self):
        self.target = 0
        self.actual = 0
        self.active = False
        self.pumpOff()

    def start(self):
        self.active = True
        self.pumpOn()

    def HWOK(self):
        if self.pumpMotor is None:
            return(False)
        else:
            return(self.pumpMotor.HWOK())
