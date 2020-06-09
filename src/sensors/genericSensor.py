class genericSensor():
    def __init__(self):
        self.id = 'nobody'
        self.errorState = False
        self.low = 0
        self.high = 999
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
        if self.val < self.low:
            self.val = self.low
        if self.val > self.high:
            self.val = self.high
        return(self.val)

    def setIncremental(self, incVal):
        """
        Set the incremental, for simulation
        """
        self.incVal = incVal

    def setLimits(self, low=0,high=999):
        """
        Set min and max limits
        """
        self.low = low
        self.high = high

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
