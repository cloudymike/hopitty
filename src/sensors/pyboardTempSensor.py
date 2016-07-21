import pyboardread
import sensors
import time

class pyboardTempSensor(sensors.genericSensor):
    def __init__(self):
        self.errorState = False
        self.id = 'pyboardTemp'
        self.val = 90
        self.devs = None
        self.device = self.connect()
        self.simulation = (self.device is None)
        self.incVal = 1.3

    def connect(self):
        try:
            self.device = pyboardread.pyboardread()
        except:
            return None

        return(self.device)

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
                self.device = self.connect()
            return(self.val)

    def HWOK(self):
        return(not self.simulation)

if __name__ == '__main__':  # pragma: no cover
    ts = pyboardTempSensor()
    print ts.getValue()
    print ts.getValue()
    time.sleep(1)
    print ts.getValue()
