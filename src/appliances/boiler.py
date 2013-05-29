#import subprocess
import appliances.genctrl
import sensors

# Manage the wort boiler
# Checks that a boil is started by checking temp, over 200F is boil
# This is not completely true, but as this sensor is less accurate
# it is close enough
# Consider to not check when boil has started once...


class boiler(appliances.genctrl):
    def __init__(self):
        self.boilerSwitch = None
        self.powerOn = False
        self.active = False
        self.unit = None
        self.target = 200
        self.unit = 'F'
        self.sensor = sensors.temperSensor()

    def __del__(self):
        self.powerOn = False
        print 'Powering down'

    def connectSwitch(self, switch):
        self.boilerSwitch = switch

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
        return(self.measure())

    def getTarget(self):
        return(self.target)

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

if __name__ == '__main__':
    testBoiler = boiler()
    testBoiler.on()
    while not testBoiler.targetMet():
        print testBoiler.get()
    for x in range(0, 15):
        print testBoiler.get()
