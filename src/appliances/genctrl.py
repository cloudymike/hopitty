'''
Created on Oct 17, 2012

@author: mikael
'''

import sensors


class genctrl():
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
        self.actual = 0  # Actual measured value, ex temp
        self.target = 0  # Target value
        self.unit = 'U'  # Unit of measure
        self.powerOn = False  # If the power is on heater/pump etc
        self.active = False  # Controller is running
        self.switch = None  # Switch object. Should have method on and off
        self.sensor = sensors.genericSensor()

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

    def measure(self):
        """
        Measure what is controlled. This dummy function is simulating
        Something trying to reach a target value, and stay there.
        Others (like pumps and time) will just go in one direction

        This functions MUST be rewritten for every controller!
        """
        if self.targetMet():
            self.actual = self.actual + 1
        else:
            self.actual = self.actual - 1

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
        pass

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
