import sys
sys.path.append('..')
import sensors
import time
import serial
import logging

analogChannel = "0";

portName = '/dev/serial/by-id/usb-Microchip_Technology_Inc._CDC_RS-232_Emulation_Demo-if00'
altPortName = '/dev/serial/by-id/pci-Microchip_Technology_Inc._CDC_RS-232_Emulation_Demo-if00'

class mashTempSensor(sensors.genericSensor):
    def __init__(self):
        self.id = 'mashTemp'
        self.errorState = False
        self.val = 100
        self.incVal = 0
        self.simulation = not self.HWOK()

    def readTemp(self):  # pragma: no cover
        try: 
            serPort = serial.Serial(portName, 19200, timeout=0.1)
        except:
            try:
                serPort = serial.Serial(altPortName, 19200, timeout=0.1)
            except:
                return(None)
        if self.simulation:
            raw = "123"
        else:
            serPort.write("adc read "+ str(analogChannel) + "\r")
            response = serPort.read(25)
            serPort.close()
        try:
            rawval = response[10:-3].strip()
            bitval = float(rawval)
            mV = bitval/1023 * 5000
            C = (mV - 500) / 10
            F = int(C * 1.8 + 32)
#            print \
#            "Raw:", rawval, \
#            "mV:{0:.0f}".format(mV), \
#            "C:{0:.2f}".format(C), \
#            "F:", F
        except:
            logging.error("Error converting MashTemp value")
            F = self.val
        return(F)

    def getValue(self):
        if not self.simulation:
            newval = self.readTemp()
            if newval is not None:
                self.val = newval
            else:
                logging.error("Read error on mash temp, using old val")
        return self.val

    def HWOK(self):
        """
        Return OK if HW USB is connected and working.
        For sensors without USB connection return true
        at all times
        """
        try: 
            serPort = serial.Serial(portName, 19200, timeout=1)
        except:
            try:
                serPort = serial.Serial(altPortName, 19200, timeout=1)
            except:
                self.simulation = True
                print("**********Mash temp sensor not found. Simulating HW")
                return(False)
        return(True)

if __name__ == '__main__':  # pragma: no cover
    t = mashTempSensor()
    if t.HWOK():
        print "HW used"
    else:
        print "Simulation used"
    for x in range(0, 30):
        print t.getValue()
        time.sleep(1)
