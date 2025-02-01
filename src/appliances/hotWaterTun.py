# import subprocess
import appliances.genctrl
import sensors.genericSensor


class hwt(appliances.genctrl.genctrl):
    def __init__(self):
        self.errorState = False  # If an error has occured
        self.hotWaterTun = None
        self.powerOn = False
        self.active = False
        self.presetTemp = 40.0
        self.unit = 'F'
        self.sensor = sensors.genericSensor.genericSensor()
        self.actual = 0  # Actual measured value, ex temp

    def __del__(self):
        self.stop()

    def connectSwitch(self, switch):
        self.hotWaterTun = switch

    def connectSensor(self, sensor):
        self.sensor = sensor

    def measure(self):
        if self.powerOn:
            incval = 5
        else:
            incval = -5
        self.sensor.setIncremental(incval)
        self.actual = self.sensor.getValue()

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def set(self, preset):
        self.presetTemp = float(preset)

    def update(self):
        if self.targetMet():
            self.off()
        else:
            self.on()

    def targetMet(self):
        if self.getActualVar() < self.presetTemp:
            return(False)
        else:
            return(True)

    def get(self):
        self.measure()
        return(self.actual)

    def getActualVar(self):
        """
        Get the actual measured value.
        Just get the value from variable, do not trigger measure
        """
        return(self.actual)

    def getTarget(self):
        return(self.presetTemp)

    def stop(self):
        self.active = False
        self.off()

    def on(self):
        if self.hotWaterTun is not None:
            try:
                self.hotWaterTun.on()
                self.clearError()
            except:
                self.forceError()

        self.powerOn = True

    def off(self):
        if self.hotWaterTun is not None:
            try:
                self.hotWaterTun.off()
                self.clearError()
            except:
                self.forceError()

        self.powerOn = False

    def HWOK(self):
        if self.hotWaterTun is None:
            return(False)
        return(self.sensor.HWOK())
