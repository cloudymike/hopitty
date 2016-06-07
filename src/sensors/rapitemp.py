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

class raspberryPiTemp():
    def __init__(self, device_file=device_file1):
        self.device_file = device_file

    def get_temperature(self, format='celsius'):
        read_temp(self.device_file, temp_c, temp_f)
        if format == 'celcius':
            return(temp_c)
        elif format == 'fahrenheit':
            return(temp_f)
        else:
            return(None)
        
    def check_device(self):
        try:
            read_temp_raw(self.device_file)
        except:
            return(False)
        return(True)
        
if __name__ == "__main__":
    while True:
        print 'TEMP 1'    
        print(read_temp(device_file1,temp_c,temp_f))
        print 'TEMP 2'
        print(read_temp(device_file2,temp_c,temp_f))
        time.sleep(10)
