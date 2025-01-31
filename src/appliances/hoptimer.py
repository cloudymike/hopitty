import time
import appliances.genctrl
import sensors.genericSensor


class hoptimer(appliances.genctrl):

    def __init__(self):
        """
        Switch is not used, just to be consistent with other modules
        """
        self.errorState = False  # If an error has occured
        self.pauseflag = False
        self.actual = 0.0
        self.target = 0.0
        self.active = False
        self.absminutes = time.localtime(time.time()).tm_sec / 60.0
        self.unit = 'min'
        self.powerOn = False
        self.sensor = sensors.genericSensor.genericSensor()

    def __del__(self):
        pass

    def measure(self):
        currmin = time.localtime(time.time()).tm_sec / 60.0
        deltamin = currmin - self.absminutes
        if deltamin < 0:
            deltamin = deltamin + 1.0
        self.absminutes = currmin
        if self.target > 0 :
            if self.pauseflag:
                self.actual = self.actual
                print('measure: {}'.format(self.actual))
            else:
                self.actual = self.actual + deltamin

    def stop(self):
        """
        Stops the controller. Reset all count values, as timers.
        De-activate the controller
        Should shut down all power as well
        to ensure that all is safe after stop
        """
        self.target = 0
        self.actual = 0
        self.active = False
        self.powerOn = False
        self.absminutes = time.localtime(time.time()).tm_sec / 60.0
        self.pauseflag = False

    def pause(self):
        """
        Pause any action, to allow a temporary pause in the brew process.
        This should be a no-action stage. Pumps should be stopped.
        heaters should keep it'd temperature. etc. It is not the same
        as stop.
        """
        self.pauseflag = True

    def start(self):
        self.active = True
        self.pauseflag = False
