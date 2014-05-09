class genericSensor():
    def __init__(self):
        self.id = 'nobody'
        self.errorState = False

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getValue(self):
        """
        Return the current sensor value
        """
        return(42)

    def hasError(self):
        """
        Return true if an error has occured
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
