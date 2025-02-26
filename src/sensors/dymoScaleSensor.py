import sys
sys.path.append('..')
import sensors.genericSensor
import time
import usb.core
import usb.util
import subprocess
from retry import retry

# DYMO 100lb scale
VENDOR_ID = 0x0922
PRODUCT_ID = 0x8007


class dymoScaleSensor(sensors.genericSensor.genericSensor):

    def __init__(self):
        self.errorState = False
        self.val = 0
        self.id = 'mashScale'
        self.simulation = False
        # find the USB device
        try:
            ret = subprocess.call('lsusb',  stdout=open('/dev/null', 'w'),
                                  stderr=subprocess.STDOUT)
        except:
            ret = 9
        if ret != 0:
            self.simulation = True
        else:
            self.dev = usb.core.find(idVendor=VENDOR_ID,
                                     idProduct=PRODUCT_ID)
            # was it found?
            if self.dev is None:
                self.simulation = True
            else:
                self.simulation = False
                try:
                    devmanufacturer = usb.util.get_string(self.dev, 256, 1)
                    devname = usb.util.get_string(self.dev, 256, 2)
                except:
                    # This have been seen failing.
                    # If so, enter simulation mode.
                    self.simulation = False

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    @retry(tries=5)
    def readVol(self):  # pragma: no cover

        if not self.dev:
            print("WARNING: No scale, try to reconnect")
            try:
                self.dev = usb.core.find(idVendor=VENDOR_ID,
                  idProduct=PRODUCT_ID)
            except:
                print("ERROR: Can not reconnect scale")
        # Check if device is connected else try to reconnect
        try:
            isActive = self.dev.is_kernel_driver_active
        except:
            print("WARNING: Scale disconnected, trying to reconnect")
            try:
                self.dev = usb.core.find(idVendor=VENDOR_ID,
                  idProduct=PRODUCT_ID)
            except:
                print("ERROR: Can not reconnect scale")

        # Simplify, but really we should just not use this.
        dev = self.dev

        interface = 0
        try:
            devOK = dev.is_kernel_driver_active is not None and dev.is_kernel_driver_active(interface) is True
        except:
            devOK = False

        if devOK:
            try:
                dev.detach_kernel_driver(interface)
            except:
                print("ERROR: Can not detach kernel driver")
            try:
                dev.set_configuration()
            except:
                print("ERROR: Can not set device configuration")
            try:
                usb.util.claim_interface(dev, interface)
            except:
                # For some unknown reason it is claimed
                # Release and re-claim
                try:
                    usb.util.release_interface(dev, interface)
                    usb.util.claim_interface(dev, interface)
                except:
                    print("ERROR: Can not claim scale interface")

        else:
            try:
                dev.set_configuration()
            except:
                print("ERROR: Can not set device configuration")

        qt = None
        for count in range(0, 10):
            # first endpoint
            endpoint = dev[0][(0, 0)][0]
            try:
                myd = dev.read(endpoint.bEndpointAddress,
                               endpoint.wMaxPacketSize)
            except:
                #print("WARNING: Scale read try {} failed".format(count))
                myd = None
            if myd is not None:
                raw_weight = myd[4] + myd[5] * 256

                DATA_MODE_GRAMS = 2
                DATA_MODE_KILOGRAMS = 3
                DATA_MODE_OUNCES = 11
                DATA_MODE_LB = 12

                if myd[2] == DATA_MODE_OUNCES:
                    ounces = raw_weight * 0.1
                    grams = 28.3495 * ounces
                elif myd[2] == DATA_MODE_GRAMS:
                    grams = raw_weight
                elif myd[2] == DATA_MODE_KILOGRAMS:
                    grams = raw_weight * 100
                elif myd[2] == DATA_MODE_LB:
                    lbs = raw_weight / 10.0
                    grams = 453.592 * lbs

                qt = grams / 946.0
                break

        try:
            usb.util.release_interface(dev, interface)
        except:
            print("ERROR: Can not release interface")

        try:
            dev.attach_kernel_driver(interface)
        except:
            print("ERROR: Can not attach kernel driver")

        return(qt)

    def getValue(self):
        if not self.simulation:
            newval = self.readVol()
            if newval is not None:
                #print("INFO: Good scale value: {}".format(newval))
                self.val = newval
            else:
                print("ERROR: Could not update volume value")
        return self.val

    def setValue(self, val):
        if self.simulation:
            self.val = val

    def HWOK(self):
        if self.simulation:
            return(False)
        else:
            self.dev = usb.core.find(idVendor=VENDOR_ID,
                                     idProduct=PRODUCT_ID)
            # was it found?
            if self.dev is None:
                return(False)
        return(True)


if __name__ == '__main__':  # pragma: no cover
    d = dymoScaleSensor()
    while (1):
        print(d.getValue())
        time.sleep(1)
