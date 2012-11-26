import time
import appliances.genctrl


class hoptimer(appliances.genctrl):

    def __init__(self):
        """
        Switch is not used, just to be consistent with other modules
        """
        self.actual = 0.0
        self.target = 0.0
        self.active = False
        self.absminutes = time.localtime(time.time()).tm_sec / 60.0
        self.unit = 'min'
        self.powerOn = 'False'
        self.sensor = hoptimer.gensensor()

    def measure(self):
        currmin = time.localtime(time.time()).tm_sec / 60.0
        deltamin = currmin - self.absminutes
        if deltamin < 0:
            deltamin = deltamin + 1.0
        self.absminutes = currmin
        if self.target > 0:
            self.actual = self.actual + deltamin
