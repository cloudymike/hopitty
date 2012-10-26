import subprocess
import genctrl


class hwt(genctrl.genctrl):
    def __init__(self, switch):
        self.hotWaterTun = switch
        self.powerOn = False
        self.active = False
        self.presetTemp = 70.0
        self.unit = 'F'
        self.currTemp = 0.0

    def __del__(self):
        self.powerOn = False
        print 'Powering down'

    def measure(self):
        return(self.currTemp)

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
        if self.currTemp < self.presetTemp:
            return(False)
        else:
            return(True)

    def get(self):
        return(self.measure())

    def getTarget(self):
        return(self.presetTemp)

    def on(self):
        self.powerOn = True

    def off(self):
        self.powerOn = False

    def stop(self):
        self.active = False
        self.off()


class hwtsim(hwt):

    def measure(self):
        if self.powerOn:
            self.currTemp = self.currTemp + 1.0
        else:
            self.currTemp = self.currTemp - 1.0
        return(self.currTemp)


class hwtHW(hwt):

    def measure(self):
        currTempStr = subprocess.check_output('../GoIO-2.28.0/mytemp/mytemp')
        try:
            self.currTemp = float(currTempStr)
        except:
            self.currTemp = 999.99
        return self.currTemp

    def on(self):
        self.hotWaterTun.on()
        self.powerOn = True

    def off(self):
        self.hotWaterTun.off()
        self.powerOn = False
