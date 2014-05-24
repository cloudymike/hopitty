import sys
sys.path.append('..')
import sensors
import time
import usb.core
import usb.util
import pygtk
pygtk.require('2.0')
import subprocess

# DYMO 100lb scale
VENDOR_ID = 0x0922
PRODUCT_ID = 0x8007


class dymoScaleSensor(sensors.genericSensor):

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
    #            print "device found: " + devmanufacturer + " " + devname
    #
    #            interface = 0
    #            if self.dev.is_kernel_driver_active(interface) is True:
    #                print "but we need to detach kernel driver"
    #                self.dev.detach_kernel_driver(interface)
    #
    #                # use the first/default configuration
    #                self.dev.set_configuration()
    #                print "claiming device"
    #                usb.util.claim_interface(self.dev, interface)

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def readVol(self):  # pragma: no cover
        dev = usb.core.find(idVendor=VENDOR_ID,
                            idProduct=PRODUCT_ID)
        interface = 0
        if dev.is_kernel_driver_active(interface) is True:
            dev.detach_kernel_driver(interface)
            # use the first/default configuration
            dev.set_configuration()
            try:
                usb.util.claim_interface(dev, interface)
            except:
                # For some unknown reason it is claimed
                # Release and re-claim
                try:
                    usb.util.release_interface(dev, interface)
                    usb.util.claim_interface(dev, interface)
                except:
                    print "ERROR: Can not claim scale interface"

        else:
            dev.set_configuration()

        qt = None
        for count in range(0, 10):
            # first endpoint
            endpoint = dev[0][(0, 0)][0]
            try:
                myd = dev.read(endpoint.bEndpointAddress,
                               endpoint.wMaxPacketSize)
            except:
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

        usb.util.release_interface(dev, interface)
        dev.attach_kernel_driver(interface)
        return(qt)

    def getValue(self):
        if not self.simulation:
            newval = self.readVol()
            if newval is not None:
                self.val = newval
            else:
                self.data.setHWerror(myid=__name__,
                                     errorText="dymoScale read error",
                                     retries=10)
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
    t = sensors.temperSensor()
    while (1):
        print d.getValue(), t.getValue()
        time.sleep(1)
