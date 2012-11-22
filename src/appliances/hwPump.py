import time
import appliances.genctrl


class hwPump(appliances.genctrl):

    def __init__(self):
        self.actual = 0.000
        self.target = 0
        self.active = False
        self.totalVol = 0
        self.powerOn = False
        self.absSec = time.time()
        self.SEC_PER_QUART = 39.0
        self.unit = 'Qt'
        self.pumpMotor = None

    def connectSwitch(self, switch):
        """
        If a switch is required, this will connect it with the devices
        The switch object needs to have a method on and a method off.
        """
        self.pumpMotor = switch

    def measure(self):
        currSec = time.time()
        deltaSec = currSec - self.absSec
        deltavol = deltaSec / self.SEC_PER_QUART
        self.absSec = currSec
        if self.powerOn:
            self.actual = self.actual + deltavol
            self.totalVol = self.actual + deltavol

    def update(self):
        self.measure()
        if self.targetMet():
            self.pumpOff()

    def pumpOn(self):
        if not self.targetMet():
            self.powerOn = True
            if self.pumpMotor != None:
                self.pumpMotor.on()

    def pumpOff(self):
        self.powerOn = False
        if self.pumpMotor != None:
            self.pumpMotor.off()

    def stop(self):
        self.target = 0
        self.actual = 0
        self.active = False
        self.pumpOff()

    def start(self):
        self.active = True
        self.pumpOn()
