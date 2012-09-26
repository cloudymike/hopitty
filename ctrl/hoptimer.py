#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess
import getopt
import sys

class hoptimer():
    
    def __init__(self):
        self.minutes=0
        self.targetMinutes=0
        self.absminutes=time.localtime(time.time()).tm_min

    def __del__(self):
        self.stop()

    def checkmins(self):
        currmin=time.localtime(time.time()).tm_min
        deltamin=currmin-self.absminutes
        print self.targetMinutes
        if deltamin < 0:
            deltamin=deltamin+60
        self.absminutes=currmin
        if self.targetMinutes > 0:
            self.minutes=self.minutes+deltamin


    def done(self):
        if self.minutes >= self.targetMinutes:
           return(True)
        else:
           return(False)

    def set(self, minutes):
        self.targetMinutes=minutes

    def get(self):
        self.checkmins()
        return(self.minutes)

    def stop(self):
        self.targetMinutes=0
        self.minutes=0

class hoptimersim(hoptimer):
    """
    The simulation version of the class
    Should do the same but increment every second instead
    of minute. Yes, this will get the values wrong but 
    speeds up the simulation to make it more useful
    """
    def __init__(self):
        self.minutes=0
        self.targetMinutes=0
        self.absminutes=time.localtime(time.time()).tm_sec

    def checkmins(self):
        currmin=time.localtime(time.time()).tm_sec
        deltamin=currmin-self.absminutes
        print self.targetMinutes
        if deltamin < 0:
            deltamin=deltamin+60
        self.absminutes=currmin
        if self.targetMinutes > 0:
            self.minutes=self.minutes+deltamin





