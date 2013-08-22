import sensors
import subprocess
import os
import signal
import dataMemcache


class mashScaleSensor(sensors.genericSensor):

    def __init__(self):
        self.myData = dataMemcache.brewData()
        self.warningCount = 0
        self.id = 'mashScale'
        self.simulation = False
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

    def getValue(self):
        if self.simulation:
            return(self.val)
        else:
            execstring = 'timeout 1 ' + self.exedir
            try:
                localstr = subprocess.check_output(execstring, shell=True)
                if float(localstr) > 65535:
                    print "Error, hold everything"
                    self.myData.setError()
                if int(localstr) > 8200:
                    print "Error hold everything"
                    self.myData.setError()

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
