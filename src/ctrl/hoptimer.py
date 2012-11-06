import time
import genctrl

class hoptimer(genctrl.genctrl):

    def __init__(self):
        self.actual = 0.0
        self.target = 0.0
        self.active = False
        self.absminutes = time.localtime(time.time()).tm_sec/60.0
        self.unit = 'min'
        self.powerOn = 'False'

    def measure(self):
        currmin = time.localtime(time.time()).tm_sec/60.0
        deltamin = currmin - self.absminutes
        if deltamin < 0:
            deltamin = deltamin + 60.0
        self.absminutes = currmin
        if self.target > 0:
            self.actual = self.actual + deltamin


class hoptimer_sim(hoptimer):
    """
    The simulation version of the class
    Should do the same but increment every second instead
    of minute. Yes, this will get the values wrong but
    speeds up the simulation to make it more useful
    """
    def __init__(self):
        self.actual = 0
        self.target = 0
        self.active = False
        self.absminutes = time.localtime(time.time()).tm_sec
        self.unit = 'sec'
        self.powerOn = False

    def measure(self):
        currmin = time.localtime(time.time()).tm_sec
        deltamin = currmin - self.absminutes
        if deltamin < 0:
            deltamin = deltamin + 60
        self.absminutes = currmin
        if self.isActive():
            self.actual = self.actual + deltamin
