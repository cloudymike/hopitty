"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons
Attribution 2.5 Canada License.
To view a copy of this license, visit
http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'May 17 2010'

# Basic imports
import time
# Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs
from Phidgets.Events.Events import ErrorEventArgs, InputChangeEventArgs
from Phidgets.Events.Events import OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit


class onePump():
    def __init__(self, usb=None, index=0):
        self.error = False
        self.usb = usb
        self.index = index
        self.errorStatus = False

    def on(self):
        if self.usb is not None:
            try:
                self.usb.setOutputState(self.index, True)
                self.clearError()
            except:
                self.forceError()

    def off(self):
        if self.usb is not None:
            try:
                self.usb.setOutputState(self.index, False)
                self.clearError()
            except:
                self.forceError()

    def HWOK(self):
        return (self.usb is not None)

    def hasError(self):
        return(self.errorStatus)

    def clearError(self):
        self.errorStatus = False

    def forceError(self):
        self.errorStatus = True


class pumpUSB():  # pragma: no cover
    def __init__(self):
        print("Initiating pumps")
        try:
            self.interfaceKit = InterfaceKit()
        except RuntimeError as e:
            print("Runtime Exception a: %s" % e.details)
            print("Exiting....")
            exit(1)
        try:
            self.interfaceKit.openPhidget()
        except PhidgetException as e:
            print("Phidget Exception b %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        try:
            self.interfaceKit.waitForAttach(1000)
        except PhidgetException as e:
            print("Phidget Exception c %i: %s" % (e.code, e.details))
            raise Exception("Timeout")
            try:
                self.interfaceKit.closePhidget()
            except PhidgetException as e:
                print("Phidget Exception d %i: %s" % (e.code, e.details))
                print("Exiting....")
                exit(1)
        self.pumplist = []
        for i in range(0, 4):
            self.pumplist.append(onePump(self.interfaceKit, i))
        print("Pumps ready")

    def getPump(self, index):
        return(self.pumplist[index])

    def getSwitch(self, index):
        """ yes it is the same as getPump, standard name use """
        return(self.pumplist[index])

    def close(self):
        self.interfaceKit.closePhidget()

if __name__ == "__main__":  # pragma: no cover

# Create an interfacekit object

    print("Opening phidget object....")
    pu = pumpUSB()
    pump0 = pu.getPump(0)
    pump1 = pu.getPump(1)
    pump2 = pu.getPump(2)
    pump3 = pu.getPump(3)

    for x in range(0, 3):
       print "Pump %d" % (x)
       pu.getPump(x).off()
       print "Pump on"
       pu.getPump(x).on()
       time.sleep(1)
       print "Pump off"
       pu.getPump(x).off() 
       time.sleep(1)


    print("Closing...")
    pu.close()

    print("Done.")
    exit(0)
