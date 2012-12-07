from x10.controllers.cm11 import CM11


class myX10(CM11):

    def simSwitch(self, X10addr):
        return(self.actuator(X10addr))
