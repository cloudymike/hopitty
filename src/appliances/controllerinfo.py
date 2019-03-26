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
        
        self.equipment = {}

    def measure(self):
        pass
    
    def targetMet(self):
        return(True)
    
    def setEquipment(self, equipment):
        self.equipment = equipment
        
    def getEquipment(self):
        return(self.equipment)
        
    def getEquipmentName(self):
        return(self.equipment['equipmentName'])

    def getEquipmentSpecs(self):
        return(self.equipment['specs'])
        
