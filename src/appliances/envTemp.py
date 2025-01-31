import appliances.genctrl
import sensors.genericSensor


class envTemp(appliances.genctrl):

    def __init__(self):
        """
        Switch is not used, just to be consistent with other modules
        """
        self.errorState = False  # If an error has occurred
        self.powerOn = False
        self.active = False
        self.target = 72
        self.unit = 'F'
        #self.sensor = sensors.envTempSensor()
        self.sensor = sensors.genericSensor.genericSensor()
        self.actual = 100

    def measure(self):
        self.actual = self.sensor.getValue()
        return(self.actual)

    def connectSensor(self, sensor):
        self.sensor = sensor

    def targetMet(self):
        """ Function for target met. Sensor only, return true"""
        return(True)

    def HWOK(self):
        """
        Return True if all USB connections are OK to the HW devices.
        """
        return(self.sensor.HWOK())
