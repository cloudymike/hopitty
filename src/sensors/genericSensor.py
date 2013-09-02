class genericSensor():
    def __init__(self):
        self.id = 'nobody'

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getValue(self):
        """
        Return the current sensor value
        """
        return(42)

    def HWOK(self):
        """
        Return OK if HW USB is connecteed and working.
        For sensors without USB connection return true
        at all times
        """
        return(True)
