'''
Created on Apr 17, 2013

@author: mikael
'''
import os
import subprocess

import appliances.genctrl
import sensors.genericSensor

empty = 0
full = 1


class dispenser(appliances.genctrl):
    '''
    Generic controller
    Use this baseclass to derive the actual controllers
    The controller has a generic sensor and switch class as well.
    '''

    def __init__(self, number=1):
        '''
        Constructor
        multiple devices may require same switch collection
        Note, controller can run but power
        could be off, as example, heater goes
        on and off, while controller is active
        '''
        self.errorState = False  # If an error has occured
        self.deviceNumber = number
        self.servo = str(number)
        self.actual = full       # Actual measured value, ex temp
        self.target = full       # Target value
        self.unit = 'U'       # Unit of measure
        self.powerOn = False  # If the power is on heater/pump etc
        self.active = False   # Controller is running
        self.switch = None    # Switch object. Should have method on and off
        self.sensor = sensors.genericSensor.genericSensor()

        try:
            ret = subprocess.call('lsusb',  stdout=open('/dev/null', 'w'),
                                  stderr=subprocess.STDOUT)
        except:
            ret = 9
        self.usbOK = (ret == 0)

        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.exe = scriptdir + '/../../UscCmd/UscCmd'

        if self.usbOK:
            self.usbOK = self.HWOK()

        # If multiple dispensers are added, these values can be set in
        # connectSwitch
        if number % 2 == 1:
            self.vFull = '8000'
            self.vEmpty = '4000'
        else:
            self.vFull = '4000'
            self.vEmpty = '8000'
        self.exeFull = self.exe + ' --servo ' + self.servo + ',' + self.vFull
        self.exeEmpty = self.exe + ' --servo ' + self.servo + ',' + self.vEmpty

        self.move()

    def measure(self):
        """
        Measure what is controlled. This dummy function is simulating
        Something trying to reach a target value, and stay there.
        Others (like pumps and time) will just go in one direction

        This functions MUST be rewritten for every controller!
        """
        pass

    def update(self):
        """
        Updates controller status
        meaning turning off or on power
        Probably a good idea to do a self.measure() first
        """
#        if self.active:
#            self.move()

        # Try to set every update
        self.move()

    def targetMet(self):
        """ Function for target met. Rewrite for each implementation"""
        return(self.actual == self.target)
        #return(True)

    def stop(self):
        """
        Stops the controller. Reset all count values, as timers.
        De-activate the controller
        Should shut down all power as well
        to ensure that all is safe after stop
        In this case return the dispenser to Full value
        """
        self.target = full
        self.move()
        self.active = False

    def move(self):
        if self.target == empty:
            if self.usbOK:
                try:
                    retval = subprocess.check_output(self.exeEmpty, shell=True)
                except:
                    pass
            self.actual = empty
        else:
            if self.usbOK:
                try:
                    retval = subprocess.check_output(self.exeFull, shell=True)
                except:
                    pass
            self.actual = full

    def HWOK(self):
        if not os.path.isfile(self.exe):
            return(False)

        if not self.usbOK:
            return (False)

        checkstring = self.exe + ' --list'
        retval = subprocess.check_output(checkstring, shell=True)
        return(retval[0] != '0')
