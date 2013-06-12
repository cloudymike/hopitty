import temper


class temperSensor():
    def __init__(self):
        self.id = 'temper'
        self.val = 150

        th = temper.TemperHandler()
        self.devs = th.get_devices()

        self.simulation = (len(self.devs) == 0)
        if len(self.devs) > 1:
            print "Error, more than one device found, using first device"
        if not self.simulation:
            self.device = self.devs[0]

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getValue(self):
        if self.simulation:
            self.val = self.val + 1.3
            if self.val > 212:
                self.val = 212
            return(self.val)
        else:
            try:
                self.val = self.device.get_temperature(format="fahrenheit")
            except:
                print "Error temper value not read, using previous value"
            return(self.val)

    def HWOK(self):
        return(not self.simulation)

if __name__ == '__main__':
    ts = temperSensor()
    print ts.getValue()
    print ts.getValue()
