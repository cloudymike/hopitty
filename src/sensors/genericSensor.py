class genericSensor():
    def __init__(self):
        self.id = 'nobody'

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getValue(self):
        return(42)
