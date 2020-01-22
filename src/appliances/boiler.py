# import subprocess
import appliances.genctrl
import sensors

class boiler(appliances.genctrl):
    """
    Manage the wort boiler
    Checks that a boil is started by checking temp, over 200F is boil
    This is not completely true, but as this sensor is less accurate
    it is close enough
    Consider to not check when boil has started once...
    """
    def __init__(self):
        self.errorState = False  # If an error has occured
        self.boilerSwitch = None
        self.powerOn = False
        self.active = False
        self.unit = None
        self.target = 200
        self.unit = 'F'
        self.sensor = sensors.genericSensor()
        self.actual = 0  # Actual measured value, ex temp

    def __del__(self):
        self.powerOn = False
        #print 'Powering down'

    def connectSwitch(self, switch):
        self.boilerSwitch = switch

    def connectSensor(self, sensor):
        self.sensor = sensor

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def set(self, preset):
        self.target = preset

    def update(self):
        if self.isActive():
            self.on()
        else:
            self.off()

    def targetMet(self):
            return(self.get() >= self.target)

    def measure(self):
        return(self.sensor.getValue())

    def get(self):
        self.actual = self.measure()
        return(self.actual)

    def getTarget(self):
        return(self.target)

    def stop(self):
        self.active = False
        self.off()

    def on(self):
        if self.boilerSwitch is not None:  # pragma: no cover
            try:
                self.boilerSwitch.on()
                self.clearError()
            except:
                self.forceError()

        self.powerOn = True
        self.sensor.setIncremental(2)

    def off(self):
        if self.boilerSwitch is not None:  # pragma: no cover
            try:
                self.boilerSwitch.off()
                self.clearError()
            except:
                self.forceError()

        self.powerOn = False

    def HWOK(self):
        if self.boilerSwitch is None:
            return(False)
        return(self.sensor.HWOK())

    def getSensor(self):
        return(self.sensor)

if __name__ == '__main__':  # pragma: no cover
    testBoiler = boiler()
    testBoiler.on()
    while not testBoiler.targetMet():
        print(testBoiler.get())
    for x in range(0, 15):
        print(testBoiler.get())
