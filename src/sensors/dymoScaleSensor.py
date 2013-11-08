import sys
sys.path.append('..')
import sensors
import time
import usb.core
import usb.util
import pygtk
pygtk.require('2.0')
import math

# DYMO 100lb scale
VENDOR_ID = 0x0922
PRODUCT_ID = 0x8007




class dymoScaleSensor(sensors.genericSensor):

    def __init__(self):
        self.simval = 0
        # find the USB device
        self.dev = usb.core.find(idVendor=VENDOR_ID,
              idProduct=PRODUCT_ID)
                # was it found?
        if self.dev is None:
            self.simulation = True
        else:
            self.simulation = False
            devmanufacturer = usb.util.get_string(self.dev, 256, 1)
            devname = usb.util.get_string(self.dev, 256, 2)
            print "device found: " + devmanufacturer + " " + devname

            interface = 0
            if self.dev.is_kernel_driver_active(interface) is True:
                print "but we need to detach kernel driver"
                self.dev.detach_kernel_driver(interface)

                # use the first/default configuration
                self.dev.set_configuration()
                print "claiming device"
                usb.util.claim_interface(self.dev, interface)

    def getValue(self):
        if self.simulation:
            return self.simval
        else:
            data = self.grab()
            if data != None:
                raw_weight = data[4] + data[5] * 256
                print raw_weight
                if data[2] == DATA_MODE_OUNCES:
                    ounces = raw_weight * 0.1
                    weight = math.ceil(ounces)
                    print_weight = "%s oz" % ounces
                elif data[2] == DATA_MODE_GRAMS:
                    grams = raw_weight
                    weight = math.ceil(grams)
                    print_weight = "%s g" % grams
                return raw_weight


    def grab(self):
        try:
            # first endpoint
            endpoint = self.dev[0][(0, 0)][0]

            # read a data packet
            attempts = 10
            data = None
            while data is None and attempts > 0:
                try:
                    data = self.dev.read(endpoint.bEndpointAddress,
                                       endpoint.wMaxPacketSize)
                except usb.core.USBError as e:
                    data = None
                    if e.args == ('Operation timed out',):
                        attempts -= 1
                        print "timed out... trying again"
                        continue

            return data
        except usb.core.USBError as e:
            print "USBError: " + str(e.args)
        except IndexError as e:
            print "IndexError: " + str(e.args)


if __name__ == '__main__':
    d = dymoScaleSensor()
    t = sensors.temperSensor()
    while (1):
        print d.getValue(), t.getValue()
        time.sleep(1)
