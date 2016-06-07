import sensors
import subprocess
import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_file1 = '/sys/bus/w1/devices/28-0000075f76ba/w1_slave'
device_file2 = '/sys/bus/w1/devices/28-0000075fdde7/w1_slave'
temp_c = 0
temp_f = 0
temp_c2 = 0
temp_f2 = 0
#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28-*')[0]
#device_file = glob.glob(device_folder + '/w1_slave')
#print device_file

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file,temp_c,temp_f):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0/5.0 +32.0
        return temp_c, temp_f
#    return
def read_fahrenheit(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_f = temp_c * 9.0/5.0 +32.0
        return temp_f
    else:
        return None

class rapithermometer(sensors.genericSensor):

    def __init__(self):
        self.errorState = False
        self.id = 'rapithermometer'
        self.simulation = False
        self.errorcount = 0
        self.val = 40.0
        self.device_file = device_file1

        try:
            temp = read_fahrenheit(self.device_file)
            if temp is None:
                self.simulation = True
        except:
            self.simulation = True

        if self.simulation:
            self.val = 70.0
            print "**********Rapberry Pi Thermometer not found, simulating HW"

    def getID(self):
        return(self.id)

    def setID(self, newID):
        self.id = newID

    def getValue(self):
        if self.simulation:
            return(self.val)
        else:
            try:
                t = read_fahrenheit(self.device_file)
                self.val = t
                self.errorcount = 0
                self.clearError()
            except:
                self.forceError()
            return(self.val)

    def setValue(self, powerOn):
        if self.simulation:
            if powerOn:
                self.val = self.val + 1.3
            else:
                self.val = self.val - 0.3
                if self.val < 70:
                    self.val = 70

    def HWOK(self):
        if self.simulation:
            return(False)
        scaleStr = subprocess.check_output(self.exedir)
        try:
            t = read_fahrenheit(self.device_file)
            if t is None:
                return(False)
        except:
            return(False)
        return(True)
