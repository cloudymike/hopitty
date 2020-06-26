'''
Created on Oct 17, 2012

@author: mikael
'''

import sensors
import switches


class mashVolume():
    '''
    Generic controller
    Use this baseclass to derive the actual controllers
    The controller has a generic sensor and switch class as well.
    '''

    def __init__(self):
        '''
        Constructor
        multiple devices may require same switch collection
        Note, controller can run but power
        could be off, as example, heater goes
        on and off, while controller is active
        '''
        self.errorState = False  # If an error has occured
        self.actual = 0  # Actual measured value, ex temp
        self.target = 0  # Target value
        self.unit = 'Qt'  # Unit of measure
        self.powerOn = False  # If the power is on heater/pump etc
        self.active = False  # Controller is running
        self.switch = switches.simSwitch
        self.sensor = sensors.dymoScaleSensor()
        self.grainVol = self.sensor.getValue()

    def __del__(self):
        self.stop()

    def empty(self):
        pass

    def full(self):
        pass

    def connectSwitch(self, switch):
        """
        If a switch is required, this will connect it with the devices
        The switch object needs to have a method on and a method off.
        """
        self.switch = switch

    def connectSensor(self, sensor):
        """
        If a sensor is required, this will connect it with the devices
        The switch object needs to have a method measure.
        """
        self.sensor = sensor

    def measure(self):
        """
        Measure what is controlled. This dummy function is simulating
        Something trying to reach a target value, and stay there.
        Others (like pumps and time) will just go in one direction

        This functions MUST be rewritten for every controller!
        """
        self.actual = self.sensor.getValue() - self.grainVol

    def update(self):
        """
        Updates controller status
        meaning turning off or on power
        Probably a good idea to do a self.measure() first
        """
        self.measure()
        if self.active:
            pass

    def targetMet(self):
        """ Function for target met. Rewrite for each implementation"""
        return(self.actual >= self.target)

    def set(self, value):
        """ Sets a target value and start controller.
        if value is 0, deactivate and stop controller
        """
        self.target = value
#        if value == 0:
#            self.stop()
#        else:
#            self.start()

    def get(self):
        """
        Get the actual measured value.
        As a side effect runs the measure command
        """
        self.measure()
        return(self.actual)

    def getActualVar(self):
        """
        Get the actual measured value.
        Just get the value from variable, do not trigger measure
        """
        return(self.actual)

    def getTarget(self):
        """
        Get the target value.
        """
        return(self.target)

    def getUnit(self):
        """
        Get the unit of measure.
        """
        return(self.unit)

    def getPowerOn(self):
        """
        Get the status of power.
        """
        return(self.powerOn)

    def stop(self):
        """
        Stops the controller. Reset all count values, as timers.
        De-activate the controller
        Should shut down all power as well
        to ensure that all is safe after stop
        """
        self.target = 0
        self.actual = 0
        self.active = False
        self.powerOn = False

    def start(self):
        self.active = True

    def isActive(self):
        return(self.active)

    def findOrAddSensor(self, clist):
        foundSensor = False
        for key, c1 in clist.items():
            if c1.sensor.getID() == "mashScale":
                foundSensor = True
                self.sensor = c1.sensor
                # print "Found mashScale sensor on", key
        if not foundSensor:
            self.sensor = sensors.dymoScaleSensor()
            # print "Created mashScale sensor"

    def pause(self):
        """
        Pause any action, to allow a temporary pause in the brew process.
        This should be a no-action stage. Pumps should be stopped.
        heaters should keep it'd temperature. etc. It is not the same
        as stop.
        """
        pass

    def HWOK(self):
        """
        Return True if all USB connections are OK to the HW devices.
        Non HW devices (as a timer) should alway return True
        """
        return(True)

    def hasError(self):
        """
        Return true if an error has occurred
        """
        return(self.errorState)

    def clearError(self):
        """
        Clear the error state
        """
        self.errorState = False

    def forceError(self):
        """
        Force the device into error state
        """
        self.errorState = True
