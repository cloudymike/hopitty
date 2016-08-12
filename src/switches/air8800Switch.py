'''
Created on March 7, 2015

@author: mikael
'''
import switches
import time
import usb.core
import logging
import cpuinfo

def is_vm():
    flags = cpuinfo.get_cpu_info()['flags']
    return('hypervisor' in flags )


class Power8800(object):
    def __init__(self):
        self.dev = None

        if not is_vm():
            try:
                self.dev = usb.core.find(idVendor=0x067b, idProduct=0x2303)
                if self.dev is None:
                    raise ValueError("Device not found")
            except:
                print "Device found...or not"

    def IsOn(self):
        # Return True if the power is currently switched on.
        ret = self.dev.ctrl_transfer(0xc0, 0x01, 0x0081, 0x0000, 0x0001)
        return ret[0] == 0xa0

    def Set(self, on):
        # If True, turn the power on, else turn it off.
        code = 0xa0 if on else 0x20
        self.dev.ctrl_transfer(0x40, 0x01, 0x0001, code, [])
        
    def HWOK(self):
        return(self.dev is not None)


class air8800Switch(switches.simSwitch):
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

        if not self.simulation:
            self.simulation = not self.power.HWOK()

        if self.simulation:
            logging.info("**********air switch not found, simulating HW")
            self.HWOKval = False
        else:
            logging.info("**********air switch found, ")
            self.HWOKval = True
        print "HWOK", self.HWOKval
        
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
    testSW = air8800Switch()
    time.sleep(2)
    testSW.on()
    time.sleep(2)
    testSW.off()
    hwok = testSW.HWOK()
    if hwok:
        logging.info("Hardware switch found with HWOK method")
    else:
        logging.info("Hardware switch not found with HWOK method")
