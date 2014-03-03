# import subprocess
import appliances.genctrl
import sensors
import dataMemcache


class hwt(appliances.genctrl):
    def __init__(self):
        self.data = dataMemcache.brewData()
        self.x10 = None  # Pointer back to the X10 so it can be reopened
#        self.hotWaterTun = switch
        self.hotWaterTun = None
        self.powerOn = False
        self.active = False
        self.presetTemp = 40.0
        self.unit = 'F'
#        self.currTemp = 70.0
        self.sensor = sensors.thermometer()

    def __del__(self):
        self.stop()
        print 'Powering down'

    def setx(self, x10):
        self.x10 = x10

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
        if self.hotWaterTun is not None:
            try:
                self.hotWaterTun.on()
                self.data.unsetHWerror(myid=__name__)
            except:
                self.data.setHWerror(myid=__name__, errorText="X10 failed")
                try:
                    self.x10.open()
                except:
                    print 'x10 open failed'

        self.powerOn = True

    def off(self):
        if self.hotWaterTun is not None:
            try:
                self.hotWaterTun.off()
                self.data.unsetHWerror(myid=__name__)
            except:
                self.data.setHWerror(myid=__name__, errorText="X10 failed")
                try:
                    self.x10.open()
                except:
                    print 'x10 open failed'

        self.powerOn = False

    def HWOK(self):
        if self.hotWaterTun is None:
            return(False)
        return(self.sensor.HWOK())
