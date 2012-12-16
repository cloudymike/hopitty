import sensors
import subprocess
import os
import signal

class mashScaleSensor(sensors.genericSensor):

    def __init__(self):
        self.id = 'mashScale'
        self.simulation = False
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.exedir = scriptdir + '/../../DigiWeight/usbscale'
        try:
            #print 'Fake scale check'
            self.scaleStr = subprocess.check_output(self.exedir)
        except:
            self.simulation = True
            self.val = 0
            print "******************Scale not found, entering simulation mode"

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
                self.scaleStr = subprocess.check_output(execstring, shell=True)
            except:
                print "Scale read error"
            #scaleStr = subprocess.check_output(self.exedir)
            #scaleStr = subprocess.check_output('timeout 1 sleep 1; echo 1', shell=True)
            qt = float(self.scaleStr) / 320
            return(qt)

    def setValue(self, val):
        if self.simulation:
            self.val = val
