# import subprocess
import appliances.genctrl
import sensors.genericSensor


class cooler(appliances.genctrl.genctrl):
    """
    Manage the wort cooler
    """
    def __init__(self):
        self.errorState = False  # If an error has occured
        self.coolerSwitch = None
        self.powerOn = False
        self.active = False
        self.target = 80
        self.unit = 'F'
        # self.sensor = sensors.temperCoolerSensor()
        # Set a generic sensor, later swap for same sensor as boiler.
        self.sensor = sensors.genericSensor.genericSensor()
        self.actual = 0  # Actual measured value, ex temp

    def __del__(self):
        self.powerOn = False

    def connectSwitch(self, switch):
        self.coolerSwitch = switch

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
            return(self.getActualVar() <= self.target)

    def measure(self):
        if self.powerOn:
            incval = -10
        else:
            incval = -1
        self.sensor.setIncremental(incval)
        self.actual = self.sensor.getValue()
        return(self.actual)

    def get(self):
        self.actual = self.measure()
        return(self.actual)

    def getTarget(self):
        return(self.target)

    def stop(self):
        self.active = False
        self.off()

    def on(self):
        if self.coolerSwitch is not None:
            self.coolerSwitch.on()
        self.powerOn = True
        self.sensor.setIncremental(-3)

    def off(self):
        if self.coolerSwitch is not None:
            self.coolerSwitch.off()
        self.powerOn = False

    def HWOK(self):
        return(self.sensor.HWOK())

if __name__ == '__main__':  # pragma: no cover
    testCooler = cooler()
    testCooler.on()
    while not testCooler.targetMet():
        print(testCooler.get())
    for x in range(0, 15):
        print(testCooler.get())
