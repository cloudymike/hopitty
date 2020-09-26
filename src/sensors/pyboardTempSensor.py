import pyboardread
import sensors
import time
import sys
import traceback

class tempSensorDict():
    """
    Create ONE object that talks to USB to minimize chatter.
    """
    def __init__(self):
        self.device = self.connect()
        self.sensorDict = {}

    def connect(self):
        try:
            self.device = pyboardread.pyboardread()
        except:
            return None
        if self.device.HWOK():
            return (self.device)
        else:
            return None

    def getSensor(self, ROM):
        """
        Create a sensor object and add it to the dict
        Connect this object to the sensor object
        Allows this object to control access to HW
        """
        self.sensorDict[ROM] = pyboardTempSensor(ROM, self.device)

        return(self.sensorDict[ROM])


class pyboardTempSensor(sensors.genericSensor):

    def __init__(self, ROM="", device=None):
        self.errorState = False
        self.id = 'temp-' + ROM
        self.val = 70
        self.devs = None
        self.ROM = ROM
        self.device = device
        self.simulation = (self.device is None)
        self.incVal = 1.3

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def setSimValue(self):
        self.val = self.val + self.incVal
        if self.val > 212:
            self.val = 212
        if self.val < 32:
            self.val = 32

    def setIncremental(self, incval):
        if self.simulation:
            self.val = self.val + incval
            if self.val > 212:
                self.val = 212
            if self.val < 32:
                self.val = 32


    def getValue(self):
        if self.simulation:
            self.setSimValue()
            return(self.val)
        else:
            try:
                self.val = self.device.get_temperature(format='fahrenheit', ROM=self.ROM)
                self.clearError()
            except:
                self.forceError()
            print("getValue temp: {}".format(self.val))
            traceback.print_stack(file=sys.stdout)
            return(self.val)

    def HWOK(self):
        return(not self.simulation)

if __name__ == '__main__':  # pragma: no cover
    tempSensors = tempSensorDict()
    ts = tempSensors.getSensor('28ff425f0216038b')
    print ts.getValue()
    print ts.getValue()
    time.sleep(1)
    print ts.getValue()
