import time
import appliances.genctrl
import sensors
import datetime
import dataMemcache


class hwPump(appliances.genctrl):

    def __init__(self):
        self.data = dataMemcache.brewData()
        self.actual = 0.000
        self.target = 0
        self.startVol = 0.000
        self.active = False
        self.totalVol = 0
        self.powerOn = False
        self.absSec = time.time()
        self.SEC_PER_QUART = 39.0
        self.unit = 'Qt'
        self.pumpMotor = None
        self.sensor = sensors.mashScaleSensor()
        # print "==========",self.sensor.getID()
        self.oldTime = datetime.datetime.now()
        self.actual = 0
        self.lastActual = 0
        self.lastCheck = datetime.datetime.now()

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
            self.sensor.setValue(self.sensor.getValue() + deltavol)
            # Error testing
            # self.sensor.setValue(self.sensor.getValue() - deltavol)
            # self.sensor.setValue(self.sensor.getValue())
            self.actual = self.sensor.getValue() - self.startVol
            if not self.checkFlow():
                print "Error: Flow not detected in ", __name__
                self.data.setError()

    def checkFlow(self):
        """
        Checks if there is a change in the volume if pups is
        supposed to be running.
        The check is done over 10 seconds to allow change
        If there has not been a check for 5 seconds, skip as well
        """
        # is this the first time to check for a while, if so, return true.

        deltaLastCheck = datetime.datetime.now() - self.lastCheck
        self.lastCheck = datetime.datetime.now()
        if deltaLastCheck > datetime.timedelta(seconds=5):
            self.oldTime = datetime.datetime.now()
            return(True)
        # If power is not on, don't check
        if not self.powerOn:
            self.oldTime = datetime.datetime.now()
            return(True)
        # if there is a change, return true
        delta = int((self.actual - self.lastActual) * 10000)
        if delta != 0:
            self.lastActual = self.actual
            self.oldTime = datetime.datetime.now()
            return(True)
        # Allow to fail for 10s,return true until 10s is up.
        elapsed = datetime.datetime.now() - self.oldTime
        if elapsed < datetime.timedelta(seconds=10):
            return(True)

        print elapsed
        return(False)

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
        self.startVol = self.sensor.getValue()
        self.active = False
        self.pumpOff()

    def start(self):
        self.active = True
        self.pumpOn()

    def findOrAddSensor(self, clist):
        foundSensor = False
        for key, c1 in clist.items():
            if c1.sensor.getID() == "mashScale":
                foundSensor = True
                self.sensor = c1.sensor
                # print "Found mashScale sensor on", key
        if not foundSensor:
            self.sensor = sensors.mashScaleSensor()
            # print "Created mashScale sensor"

    def HWOK(self):
        if self.pumpMotor == None:
            return(False)
        else:
            if self.pumpMotor.HWOK():
                return(self.sensor.HWOK())
            else:
                return(False)

    def pause(self):
        """
        Pause any action, to allow a temporary pause in the brew process.
        This should be a no-action stage. Pumps should be stopped.
        heaters should keep it'd temperature. etc. It is not the same
        as stop.
        """
        self.pumpOff()


class wortPump(hwPump):

    def measure(self):
        currSec = time.time()
        deltaSec = currSec - self.absSec
        deltavol = deltaSec / self.SEC_PER_QUART
        self.absSec = currSec
        if self.powerOn:
            sensorValue = self.sensor.getValue()
            self.sensor.setValue(sensorValue - deltavol)
            # self.sensor.setValue(sensorValue)
            self.actual = self.startVol - sensorValue
            if not self.checkFlow():
                print "Error: Flow not detected in ", __name__
                self.data.setError()
