from x10.controllers.cm11 import CM11


class myX10(CM11):

    def getSwitch(self, X10addr):
        print "myX10.getswitch", X10addr
        return(self.actuator(X10addr))
