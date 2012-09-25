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

    def checkmins(self):
        currmin=time.localtime(time.time()).tm_min
        deltamin=currmin-self.absminutes
        if deltamin < 0:
            deltamin=deltamin+60
        self.absminutes=currmin
        if self.targetMinutes > 0:
            self.minutes=self.minutes+deltamin


    def done(self):
        if self.minutes >= self.targetMinues:
           return(True)
        else:
           return(False)

    def set(self, minutes):
        self.targetMinutes=minutes

    def get(self):
        self.checkmins()
        return(self.minutes)






