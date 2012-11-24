import subprocess
import appliances.genctrl


class boiler(appliances.genctrl):
    def __init__(self):
        self.boilerSwitch = None
        self.powerOn = False
        self.active = False
        self.unit = 'None'
        self.sensor = boiler.gensensor()


    def __del__(self):
        self.powerOn = False
        print 'Powering down'

    def connectSwitch(self, switch):
        self.boilerSwitch = switch

    def measure(self):
        return(1)

    def status(self):
        if self.powerOn:
            return 'On'
        else:
            return 'Off'

    def set(self, preset):
        pass

    def update(self):
        if self.isActive():
            self.on()
        else:
            self.off()

    def targetMet(self):
            return(True)

    def get(self):
        return(self.measure())

    def getTarget(self):
        return(1)

    def stop(self):
        self.active = False
        self.off()

    def on(self):
        if self.boilerSwitch != None:
            self.boilerSwitch.on()
        self.powerOn = True

    def off(self):
        if self.boilerSwitch != None:
            self.boilerSwitch.off()
        self.powerOn = False
