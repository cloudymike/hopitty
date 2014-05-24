'''
Created on Oct 25, 2012

@author: mikael
'''
import subprocess
import os
import switches
import time


class coolerSwitch(switches.simSwitch):
    '''
    Simulated switch. Does not do a lot of things except fullfills the
    required methods of a switch object.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.simulation = False
        self.errorStatus = False
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.exe = scriptdir + '/../../coolerUSB/coolerUSB'
        print self.exe
        self.coolerOn = self.exe + ' 1'
        self.coolerOff = self.exe + ' 0'
        try:
            returnCode = subprocess.call(self.exe)
            if returnCode != 0:
                self.simulation = True
        except:
            self.simulation = True

        if self.simulation:
            print "**********Cooler switch not found, simulating HW"
        else:
            print "**********Cooler switch found, "

    def on(self):
        try:
            if self.simulation:
                returnCode = 0
            else:
                returnCode = subprocess.call([self.exe, "1"])
        except:
            returnCode = 1
        if returnCode != 0:
            self.forceError()
        else:
            self.clearError()

    def off(self):
        try:
            if self.simulation:
                returnCode = 0
            else:
                returnCode = subprocess.call([self.exe, "0"])
        except:
            returnCode = 1
        if returnCode != 0:
            self.forceError()
        else:
            self.clearError()

    def HWOK(self):
        try:
            returnCode = subprocess.call(self.exe)
            return(returnCode == 0)
        except:
            return(False)

    def hasError(self):
        return(self.errorStatus)

    def clearError(self):
        self.errorStatus = False

    def forceError(self):
        self.errorStatus = True

if __name__ == '__main__':  # pragma: no cover
    testSW = coolerSwitch()
    time.sleep(2)
    testSW.on()
    time.sleep(2)
    testSW.off()
    hwok = testSW.HWOK()
    if hwok:
        print "Hardware switch found with HWOK method"
    else:
        print "Hardware switch not found with HWOK method"
