'''
Created on Nov 20, 2013

@author: mikael
'''
# import subprocess
import appliances.genctrl
import sensors
import switches


class mashHeater(appliances.genctrl):
    """
    Manage the mash heater.
    Initial version, just check temperature.
    """
    def __init__(self):
        self.errorState = False  # If an error has occurred
        self.switch = switches.simSwitch()
        self.powerOn = False
        self.active = False
        self.target = 150
        self.unit = 'F'
        self.sensor = sensors.pyboardTempSensor()
        self.actual = 100

    def measure(self):
        self.actual = self.sensor.getValue()
        return(self.actual)

    def targetMet(self):
        """ Function for target met. Sensor only, return true"""
        return(True)

    def HWOK(self):
        """
        Return True if all USB connections are OK to the HW devices.
        """
        return(self.sensor.HWOK())
