class genericSensor():
    def __init__(self):
        self.id = 'nobody'
        self.errorState = False
        self.val = 100
        self.incVal = 0

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getValue(self):
        """
        Return the current sensor value
        """
        self.val = self.val + self.incVal
        return(self.val)

    def setIncremental(self, incVal):
        """
        Set the incremental, for simulation
        """
        self.incVal = incVal

    def hasError(self):
        """
        Return true if an error has occurred
        """
        return(self.errorState)

    def clearError(self):
        """
        Clear the error state
        """
        self.errorState = False

    def forceError(self):
        """
        Force the device into error state
        """
        self.errorState = True

    def HWOK(self):
        """
        Return OK if HW USB is connecteed and working.
        For sensors without USB connection return true
        at all times
        """
        return(True)
