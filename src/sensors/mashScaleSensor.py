import sensors
import subprocess
import os

class mashScaleSensor(sensors.genericSensor):
    def __init__(self):
        self.id = 'mashScale'
        self.simulation = False
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.exedir = scriptdir + '/../../DigiWeight/usbscale'
        try:
            scaleStr = subprocess.check_output(self.exedir)
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
            scaleStr = subprocess.check_output(self.exedir)
            qt = float(scaleStr) / 320
            return(qt)
    
    def setValue(self,val):
        if self.simulation:
            self.val = val
