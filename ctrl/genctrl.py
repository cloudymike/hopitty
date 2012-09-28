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
        self.actual=0
        self.target=0
        self.active=False

    def __del__(self):
        self.stop()

    def update(self):
        if self.Active:
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
        self.update()
        return(self.actual)

    def stop(self):
        self.targetMinutes = 0
        self.minutes = 0
        self.active = False

    def start(self):
        self.active = True

    def isActive(self):
        return(self.active)




