import sensors
import subprocess
import os
import dataMemcache


class thermometer(sensors.genericSensor):

    def __init__(self):
        self.id = 'thermometer'
        self.simulation = False
        self.errorcount = 0
        self.data = dataMemcache.brewData()
        self.val = 40.0

        scriptdir = os.path.dirname(os.path.abspath(__file__))
        self.exedir = scriptdir + '/../../mytemp/mytemp'
        try:
            scaleStr = subprocess.check_output(self.exedir)
            if scaleStr == 'No Go devices found.\n':
                self.simulation = True
        except:
            self.simulation = True

        if self.simulation:
            self.val = 70.0
            print "**********Thermometer not found, simulating HW"

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getValue(self):
        if self.simulation:
            return(self.val)
        else:
            scaleStr = subprocess.check_output(self.exedir)
            try:
                t = float(scaleStr)
                self.val = t
                self.errorcount = 0
                self.data.unsetHWerror(id=__name__)
            except:
                self.data.setHWerror(id=__name__,\
                                     errorText="Thermometer read error",\
                                     retries=10)
            return(self.val)

    def setValue(self, powerOn):
        if self.simulation:
            if powerOn:
                self.val = self.val + 1.3
            else:
                self.val = self.val - 0.3
                if self.val < 70:
                    self.val = 70

    def HWOK(self):
        if self.simulation:
            return(False)
        scaleStr = subprocess.check_output(self.exedir)
        try:
            t = float(scaleStr)
        except:
            return(False)
        return(True)
