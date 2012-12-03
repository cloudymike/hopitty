import sensors
import subprocess
import os

class thermometer(sensors.genericSensor):
    def __init__(self):
        self.id = 'thermometer'
        self.simulation = False
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.exedir = scriptdir + '/../../GoIO-2.28.0/mytemp/mytemp'
        try:
            scaleStr = subprocess.check_output(self.exedir)
        except:
            self.simulation = True
            self.val = 0
            print "******************Thermometer not found, entering simulation mode"
            
    def getID(self):
        return(self.id)
        
    def setID(self, newID):
        self.id = newID
        
    def getValue(self):
        if self.simulation:
            return(self.val)
        else:
            scaleStr = subprocess.check_output(self.exedir)
            t = float(scaleStr)
            return(t)
    
    def setValue(self,val):
        if self.simulation:
            self.val = val
