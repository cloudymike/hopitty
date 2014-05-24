import switches
from x10.controllers.cm11 import CM11


class myX10(CM11):

    def getSwitch(self, X10addr):
        print "myX10.getswitch", X10addr
        return(self.actuator(X10addr))
        # return(self.X10Switch(X10addr))


# class X10Switch(switches.simSwitch):
#    def __init__(self, X10connection, addr):
#        pass

if __name__ == '__main__':  # pragma: no cover
    x10 = myX10('/dev/serial/by-id/usb-Prolific_Technology'
                '_Inc._USB-Serial_Controller-if00-port0')
    x10.open()
    testSW = x10.getSwitch('H1')
