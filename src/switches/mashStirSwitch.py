'''
Created on Nov 20, 2013

@author: mikael
'''
import subprocess
import os
import switches
import time
import dataMemcache


class mashStirSwitch(switches.simSwitch):
    '''
    Simulated switch. Does not do a lot of things except fullfills the
    required methods of a switch object.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.simulation = False
        self.data = dataMemcache.brewData()
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.exe = scriptdir + '/../../mashStirUSB/mashStirUSB'
        print self.exe
        self.mashStirOn = self.exe + ' 1'
        self.mashStirOff = self.exe + ' 0'
        try:
            returnCode = subprocess.call(self.exe)
            if returnCode != 0:
                self.simulation = True
        except:
            self.simulation = True

        if self.simulation:
            print "**********mashStir switch not found, simulating HW"
        else:
            print "**********mashStir switch found, "

    def on(self):
        try:
            if self.simulation:
                returnCode = 0
            else:
                returnCode = subprocess.call([self.exe, "1"])
        except:
            returnCode = 1
        if returnCode != 0:
            self.data.setHWerror(myid=__name__,
                                 errorText="mashStir switch failing")
        else:
            self.data.unsetHWerror(myid=__name__)

    def off(self):
        try:
            if self.simulation:
                returnCode = 0
            else:
                returnCode = subprocess.call([self.exe, "0"])
        except:
            returnCode = 1
        if returnCode != 0:
            self.data.setHWerror(myid=__name__,
                                 errorText="mashStir switch failing")
        else:
            self.data.unsetHWerror(myid=__name__)

    def HWOK(self):
        try:
            returnCode = subprocess.call(self.exe)
            return(returnCode == 0)
        except:
            return(False)

if __name__ == '__main__':
    testSW = mashStirSwitch()
    time.sleep(2)
    testSW.on()
    time.sleep(2)
    testSW.off()
    hwok = testSW.HWOK()
    if hwok:
        print "Hardware switch found with HWOK method"
    else:
        print "Hardware switch not found with HWOK method"
