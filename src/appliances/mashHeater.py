'''
Created on Nov 20, 2013

@author: mikael
'''
# import subprocess
import appliances.genctrl
import sensors.genericSensor


class mashHeater(appliances.genctrl):
    """
    Manage the mash heater.
    Initial version, just check temperature.
    """
    def __init__(self):
        self.errorState = False  # If an error has occurred
        self.switch = None
        self.powerOn = False
        self.active = False
        self.target = 150.0
        self.unit = 'F'
        self.sensor = sensors.genericSensor.genericSensor()
        self.simulation = False
        self.actual = 70.0

    def connectSensor(self, sensor):
        """
        If a sensor is required, this will connect it with the devices
        The switch object needs to have a method measure.
        """
        self.sensor = sensor
        self.simulation = not self.HWOK()



    def set(self, value):
        self.target = float(value)

    def simValue(self):
        """ Create a sensor simulator """
        if self.active:
            if self.powerOn:
                return(self.actual + 1)
            else:
                return(self.actual - 1)
        else:
            if self.actual > 60:
                self.actual = self.actual - 1
            return(self.actual)

    def measure(self):
        if self.simulation:
             self.actual = self.simValue()
        else:
            self.actual = self.sensor.getValue()
        return(self.actual)

    def update(self):
        if self.measure() < self.target:
            self.pumpOn()
        else:
            self.pumpOff()

    def pumpOn(self):
        self.powerOn = True
        if self.switch is not None:
            self.switch.on()

    def pumpOff(self):
        self.powerOn = False
        if self.switch is not None:
            self.switch.off()

    def stop(self):
        self.active = False
        self.pumpOff()

    def targetMet(self):
        """ Function for target met. Return True, as we will not wait for this temp"""
        return(True)

    def HWOK(self):
        """
        Return True if all USB connections are OK to the HW devices.
        As the appliance has gone into simulation, this has extra print statements
        Can be removed later
        Also, do not check for switch as this is checked in other places, for pumps.
        """
        if self.sensor is None:
            return(False)
        elif not self.sensor.HWOK():
            return(False)
        else:
            return(True)

