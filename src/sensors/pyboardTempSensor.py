import pyboardread
import sensors
import time

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

        return (self.device)

    def getSensor(self, ROM):
        """
        Create a sensor object and add it to the dict
        Connect the device to the sensor object
        
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
        self.simulation = (self.device is None) or not self.device.HWOK()
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

    def getValue(self):
        if self.simulation:
            self.setSimValue()
            return(self.val)
        else:
            try:
                self.val = self.device.get_temperature(format="fahrenheit")
                self.clearError()
            except:
                self.forceError()
                # self.device = self.connect()
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
