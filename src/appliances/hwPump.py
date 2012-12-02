import time
import appliances.genctrl

class mashScaleSensor(appliances.genExtSensor):
    def __init__(self):
        self.id = 'mashScale'
        self.val = 0
            
    def getID(self):
        return(self.id)
        
    def setID(self, newID):
        self.id = newID
        
    def getValue(self):
        return(self.val)
    
    def setValue(self,val):
        self.val = val
        #print "Mash Water Volume:", int(self.val * 100) 


class hwPump(appliances.genctrl):
    

    def __init__(self):
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
        self.sensor = hwPump.gensensor()

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
            self.actual = self.sensor.getValue() - self.startVol

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
                #print "Found mashScale sensor on", key
        if not foundSensor:
            self.sensor = mashScaleSensor()
            #print "Created mashScale sensor"


class wortPump(hwPump):

    def measure(self):
        currSec = time.time()
        deltaSec = currSec - self.absSec
        deltavol = deltaSec / self.SEC_PER_QUART
        self.absSec = currSec
        if self.powerOn:
            self.sensor.setValue(self.sensor.getValue() - deltavol)
            self.actual = self.startVol - self.sensor.getValue()

