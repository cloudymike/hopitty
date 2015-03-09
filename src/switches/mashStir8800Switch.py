'''
Created on March 7, 2015

@author: mikael
'''
import switches
import time
import usb.core


class Power8800(object):
    def __init__(self):
        # Find the device.
        self.dev = usb.core.find(idVendor=0x067b, idProduct=0x2303)
        if self.dev is None:
            raise ValueError("Device not found")

    def IsOn(self):
        # Return True if the power is currently switched on.
        ret = self.dev.ctrl_transfer(0xc0, 0x01, 0x0081, 0x0000, 0x0001)
        return ret[0] == 0xa0

    def Set(self, on):
        # If True, turn the power on, else turn it off.
        code = 0xa0 if on else 0x20
        self.dev.ctrl_transfer(0x40, 0x01, 0x0001, code, [])


class mashStir8800Switch(switches.simSwitch):
    '''
    Simulated switch. Does not do a lot of things except fullfills the
    required methods of a switch object.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.simulation = False
        self.errorStatus = False
        self.HWOKval = False

        try:
            self.power = Power8800()
        except:
            self.simulation = True

        if self.simulation:
            print "**********mashStir switch not found, simulating HW"
            self.HWOKval = False
        else:
            print "**********mashStir switch found, "
            self.HWOKval = True

    def on(self):
        returnCode = 0
        try:
            if not self.simulation:
                self.power.Set(True)
        except:
            returnCode = 1
        if returnCode != 0:
            self.forceError()
        else:
            self.clearError()

    def off(self):
        returnCode = 0
        try:
            if not self.simulation:
                self.power.Set(False)
        except:
            returnCode = 1
        if returnCode != 0:
            self.forceError()
        else:
            self.clearError()

    def HWOK(self):
        return(self.HWOKval)

    def hasError(self):
        return(self.errorStatus)

    def clearError(self):
        self.errorStatus = False

    def forceError(self):
        self.errorStatus = True


if __name__ == '__main__':  # pragma: no cover
    testSW = mashStir8800Switch()
    time.sleep(2)
    testSW.on()
    time.sleep(2)
    testSW.off()
    hwok = testSW.HWOK()
    if hwok:
        print "Hardware switch found with HWOK method"
    else:
        print "Hardware switch not found with HWOK method"
