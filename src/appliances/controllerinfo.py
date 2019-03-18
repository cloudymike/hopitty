import time
import appliances.genctrl
import sensors


class controllerinfo(appliances.genctrl):

    def __init__(self):
        """
        Used to hold info about the controllerinfo
        As example, this can hold controller type and name etc.
        """
        self.errorState = False  # If an error has occured
        self.actual = 0.0
        self.target = 0.0
        self.active = False
        self.unit = 'U'
        self.powerOn = 'False'
        self.sensor = sensors.genericSensor()
        
        self.equipmentName = ''

    def measure(self):
        pass
    
    def targetMet(self):
        return(True)
    
    def setEquipmentName(self, equipment):
        self.equipmentName = equipment
        
    def getEquipmentName(self):
        return(self.equipmentName)
