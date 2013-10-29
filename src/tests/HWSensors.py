import sensors
import sys

def countFails(scale, count):
    zeros = 0
    exceptions = 0

    for x in range(0, count):

        try:
            val = scale.getRaw()
            if int(val) == 0:
                zeros = zeros + 1
                sys.stdout.write("0")
            else:
                sys.stdout.write(".")
        except:
            exceptions = exceptions + 1;
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
        countFails(scale, 100)
    else:
        print "No HW"
