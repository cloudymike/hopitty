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

    def update(self):
        """
        Updates the measured value AND updates controller status
        meaning turning off or on power
        """
        if self.active:
            if self.targetMet():
                self.actual = self.actual + 1
            else:
                self.actual = self.actual - 1

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
        As a side effect runs the update command (is this not bad?)
        Maybe better to break up into measure and control.
        get could do measure. (and so will control)
        """
        self.update()
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




