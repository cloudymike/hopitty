'''
Created on Sep 03 2015

@author: mikael
'''
# import subprocess
import appliances.genctrl
import sensors.genericSensor


class plateValve(appliances.genctrl.genctrl):
    """
    Manage the boilervalve
    """
    def __init__(self):
        self.errorState = False  # If an error has occured
        self.switch = None
        self.powerOn = False
        self.active = False
        self.target = 80
        self.unit = 'F'
        # self.sensor = sensors.temperboilerValveSensor()
        # Set a generic sensor, later swap for same sensor as boiler.
        self.sensor = sensors.genericSensor.genericSensor()
        self.actual = 0  # Actual measured value, ex temp

    def connectSwitch(self, switch):
        """
        If a switch is required, this will connect it with the devices
        The switch object needs to have a method on and a method off.
        """
        self.switch = switch

    def measure(self):
        self.actual = 0

    def targetMet(self):
        return(True)

    def update(self):
        if self.powerOn:
            self.on()
        else:
            self.off()

    def on(self):
        self.powerOn = True
        if self.switch is not None:
            self.switch.on()

    def off(self):
        self.powerOn = False
        if self.switch is not None:
            self.switch.off()

    def stop(self):
        self.target = 0
        self.actual = 0
        self.active = False
        self.off()

    def start(self):
        self.active = True
        self.on()

    def HWOK(self):
        if self.switch is None:
            return(False)
        else:
            return(self.switch.HWOK())

    def __del__(self):
        self.powerOn = False
        #print 'Powering down'

    def status(self):
        if self.on:
            return 'On'
        else:
            return 'Off'


if __name__ == '__main__':  # pragma: no cover
    testplateValve = plateValve()
    testplateValve.on()
    print testplateValve.get()
    testplateValve.off()
    print testplateValve.get()
