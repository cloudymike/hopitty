# Rugged design of Dymo Scale sensor that should be able
# to recover from a number of failure situations 

import usb.core
import usb.util
import time
import logging

VENDOR_ID  = 0x0922
PRODUCT_ID = 0x8007

class dymorugged(object):

    def __init__(self):
        self.errorState = False
        self.val = 0
        self.id = 'mashScale'
        self.simulation = False
        self.device = None
        self.endpoint = None

        self.initializeDevice()
        if self.device is None:
            self.simulation = True



    def initializeDevice(self):
        try:
            self.device = usb.core.find(idVendor=VENDOR_ID,
                                    idProduct=PRODUCT_ID)

            if self.device.is_kernel_driver_active(0):
                self.device.detach_kernel_driver(0)

            self.device.set_configuration()

            # Looks like we do not need to claim interface. KISS
            #usb.util.claim_interface(dev, interface)

            self.endpoint = self.device[0][(0,0)][0]
        except:
            logging.warning("Device with VendorID: {} and ProductID: {} not initialized".format(VENDOR_ID, PRODUCT_ID))

    def releaseDevice(self):
        logging.info("Releasing scale interface")
        try:
            usb.util.release_interface(self.device, 0)
            self.device.attach_kernel_driver(0)
        except:
            logging.warning("Scale not released")

    def reInitialize(self):
        self.releaseDevice()
        self.initializeDevice()

    def readScale(self):
        '''
        Read the scale
        If not able to read, first retry a few times then return None
        '''
        attempts = 10
        data = None
        error = 'unknown'
        while data is None and attempts > 0:
            try:
                if self.device is None:
                    logging.warning("Scale USB, no device")
                    break
                data = self.device.read(self.endpoint.bEndpointAddress,
                                        self.endpoint.wMaxPacketSize)
            except usb.core.USBError as e:
                data = None
                attempts -= 1
                if (e.args == ('Operation timed out',)) or (e.args == (16, 'Resource busy')) or (e.args == (75, 'Overflow')):
                    logging.info("Acceptable Scale USB error: {}".format(e.args))
                else:
                    logging.warning("New Scale USB error: {}".format(e.args))

        return(data)

    def readVol(self):
        '''
        Read the scale and translate the value to quarts
        If there is an error try to reinitialize a  few times
        If scale can not be read, return None and let getValue deal with error
        '''
        attempts = 3
        data = None
        while data is None and attempts > 0:
            data = self.readScale()
            if data is None:
                logging.warning("Scale not read, trying to reinitialize")
                self.reInitialize()
                attempts -= 1
        if data is None:
            return(None)
        else:
            raw_weight = data[4] + (256 * data[5])
            DATA_MODE_GRAMS = 2
            DATA_MODE_KILOGRAMS = 3
            DATA_MODE_OUNCES = 11
            DATA_MODE_LB = 12

            VAL_ZERO = 2
            VAL_UNSTABLE = 3
            VAL_POSITIVE = 4
            VAL_NEGATIVE = 5

            if data[2] == DATA_MODE_OUNCES:
                ounces = raw_weight * 0.1
                grams = 28.3495 * ounces
            elif data[2] == DATA_MODE_GRAMS:
                grams = raw_weight
            elif data[2] == DATA_MODE_KILOGRAMS:
                grams = raw_weight * 100
            elif data[2] == DATA_MODE_LB:
                lbs = raw_weight / 10.0
                grams = 453.592 * lbs
            else:
                return(None)
        if data[1] == VAL_NEGATIVE:
            grams = -1 * grams
        qt = grams / 946.0
        return(qt)

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getValue(self):
        if not self.simulation:
            newval = self.readVol()
            if newval is not None:
                #print("INFO: Good scale value: {}".format(newval))
                self.val = newval
            else:
                logging.warning("Could not update volume value")
        return self.val

    def setValue(self, val):
        if self.simulation:
            self.val = val

    def HWOK(self):
        if self.simulation:
            return(False)
        else:
            try:
                dev = usb.core.find(idVendor=VENDOR_ID,
                                     idProduct=PRODUCT_ID)
            except:
                dev = None
            # was it found?
            if dev is None:
                logging.warning("Device with VendorID: {} and ProductID: {} not found".format(VENDOR_ID, PRODUCT_ID))
                return(False)
        return(True)



if __name__ == '__main__':  # pragma: no cover
    loglevel = logging.DEBUG
    d = dymorugged()
    while (1):
        print(d.getValue())
        time.sleep(1)
