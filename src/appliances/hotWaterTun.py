#import subprocess
import appliances.genctrl
import sensors


class hwt(appliances.genctrl):
    def __init__(self):
#        self.hotWaterTun = switch
        self.hotWaterTun = None
        self.powerOn = False
        self.active = False
        self.presetTemp = 70.0
        self.unit = 'F'
#        self.currTemp = 70.0
        self.sensor = sensors.thermometer()

    def __del__(self):
        self.powerOn = False
        print 'Powering down'

    def connectSwitch(self, switch):
        self.hotWaterTun = switch

    def measure(self):
        self.sensor.setValue(self.powerOn)
        return(self.sensor.getValue())

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
        if self.sensor.getValue() < self.presetTemp:
            return(False)
        else:
            return(True)

    def get(self):
        return(self.measure())

    def getTarget(self):
        return(self.presetTemp)

    def stop(self):
        self.active = False
        self.off()

    def on(self):
        if self.hotWaterTun != None:
            self.hotWaterTun.on()
        self.powerOn = True

    def off(self):
        if self.hotWaterTun != None:
            self.hotWaterTun.off()
        self.powerOn = False
