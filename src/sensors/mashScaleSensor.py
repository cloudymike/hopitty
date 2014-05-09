import sensors
import subprocess
import os
import random


class mashScaleSensor(sensors.genericSensor):

    def __init__(self):
        self.errorState = False
        self.errorTesting = False
        self.errorModeFailing = False
        self.warningCount = 0
        self.id = 'mashScale'
        self.simulation = False
        self.oldval = 0
        self.val = 0
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.exedir = scriptdir + '/../../DigiWeight/usbscale'
        try:
            # print 'Fake scale check'
            self.scaleStr = subprocess.check_output(self.exedir)
        except:
            self.simulation = True
            self.val = 0
            print "**********Scale not found, simulating HW"

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getRaw(self):
        execstring = 'timeout 1 ' + self.exedir
        return(subprocess.check_output(execstring, shell=True))

    def getValue(self):
        if self.simulation:
            if self.errorModeFailing:
                randomrange = 1
            else:
                randomrange = 2

            if self.errorTesting:
                if random.randrange(0, randomrange) == 0:
                    return(self.oldval)
            self.oldval = self.val
            return(self.val)
        else:
            execstring = 'timeout 1 ' + self.exedir
            try:
                localstr = subprocess.check_output(execstring, shell=True)
                if float(localstr) > 65534:
                    print "Error, hold everything"
                    self.forceError()
                if int(localstr) > 8200:
                    print "Error hold everything"
                    self.forceError()

                if int(localstr) == 0:
                    print "Warning: Scale value 0 return previous value"
                    self.warningCount = self.warningCount + 1
                else:
                    self.scaleStr = localstr
            except:
                print "Warning: Scale read error"
                self.warningCount = self.warningCount + 1
            qt = float(self.scaleStr) / 320
            return(qt)

    def setValue(self, val):
        if self.simulation:
            self.val = val

    def HWOK(self):
        return(not self.simulation)
