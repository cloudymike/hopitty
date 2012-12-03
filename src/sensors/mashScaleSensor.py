import sensors

class mashScaleSensor(sensors.genericSensor):
    def __init__(self):
        self.id = 'mashScale'
        self.val = 0
            
    def getID(self):
        return(self.id)
        
    def setID(self, newID):
        self.id = newID
        
    def getValue(self):
        return(self.val)
    
    def setValue(self,val):
        self.val = val
        #print "Mash Water Volume:", int(self.val * 100) 

