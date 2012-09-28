#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess
import getopt
import sys

class genctrl():
    
    def __init__(self):
        self.actual=0     # Actual measured value, ex temp
        self.target=0     # Target value
        self.active=False # Controller is running
                          # Note, controller can run but power
                          # could be off, as example, heater goes
                          # on and off, while controller is active

    def __del__(self):
        self.stop()

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
        self.target=value
        if value == 0:
            self.stop()
        else:
            self.start()

    def get(self):
        """
        Get the actual measured value.
        As a side effect runs the measure command 
        """
        self.measure()
        return(self.actual)

    def stop(self):
        """
        Stops the controller. Should shut down all power as well
        to ensure that all is safe after stop
        """
        self.target = 0
        self.actual = 0
        self.active = False

    def start(self):
        self.active = True

    def isActive(self):
        return(self.active)




