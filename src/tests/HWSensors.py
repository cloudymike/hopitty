import sys
sys.path.append('..')

import sensors
import switches


def countFails(scale, count):
    zeros = 0
    exceptions = 0

    drone1 = sensors.thermometer()
    drone2 = sensors.temperSensor()
    switch1 = switches.coolerSwitch()
    switch2 = switches.myX10('/dev/serial/by-id/usb-Prolific_Technology'
                                 '_Inc._USB-Serial_Controller-if00-port0')
    switch3 = switches.pumpUSB()

    for x in range(0, count):

        try:
            d1 = drone1.getValue()
        except:
            sys.stdout.write('v')
        try:
            d2 = drone2.getValue()
        except:
            sys.stdout.write('t')
        try:
            s1 = switch1.off()
        except:
            sys.stdout.write('c')
        try:
            s2 = switch2.off()
        except:
            sys.stdout.write('x')
        try:
            s3 = switch3.off()
        except:
            sys.stdout.write('u')
        try:
            val = scale.getRaw()
            if int(val) == 0:
                zeros = zeros + 1
                sys.stdout.write("0")
            else:
                sys.stdout.write(".")
        except:
            exceptions = exceptions + 1
            sys.stdout.write("*")

        sys.stdout.flush()
        if x % 25 == 24:
            print ""

    print ""
    print "Exceptions:", exceptions
    print "Zeros     :", zeros


if __name__ == "__main__":
    scale = sensors.mashScaleSensor()

    if scale.HWOK():
        countFails(scale, 26)
    else:
        countFails(scale, 1)
        print "No HW"
