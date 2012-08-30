#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess
import getopt
import sys


class hwt:
    def __init__(self):
        self.powerOn=False
        self.currTemp=70
        self.setTemp=70

    def temperature(self):
        return(self.currTemp)

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def setTemp(self,temperature):
        self.setTemp=temperature




