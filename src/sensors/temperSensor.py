import temper
import dataMemcache


class temperSensor():
    def __init__(self):
        self.id = 'temper'
        self.val = 90
        self.devs = None
        self.device = self.connect()
        self.simulation = (self.device is None)
        self.data = dataMemcache.brewData()

    def connect(self):
        try:
            th = temper.TemperHandler()
            self.devs = th.get_devices()
        except:
            return None

        if (len(self.devs) == 0):
            return None

        if len(self.devs) > 1:
            print "Error, more than one device found, using first device"
        return(self.devs[0])

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def setSimValue(self):
        self.val = self.val + 1.3
        if self.val > 212:
            self.val = 212

    def getValue(self):
        if self.simulation:
            self.setSimValue()
            return(self.val)
        else:
            try:
                self.val = self.device.get_temperature(format="fahrenheit")
                self.data.unsetHWerror(myid=__name__)
            except:
                self.data.setHWerror(myid=__name__,
                                     errorText="temper value fail")
                self.device = self.connect()
            return(self.val)

    def HWOK(self):
        return(not self.simulation)

if __name__ == '__main__':
    ts = temperSensor()
    print ts.getValue()
    print ts.getValue()
