import sys
sys.path.append('..')
import sensors
import time
import serial
import logging
import json
import pprint

portName = \
    '/dev/serial/by-id/usb-Micro_Python_Pyboard_Virtual_Comm_Port_in_FS_Mode_000000000011-if01'
altName = \
    '/dev/serial/by-id/pci-Micro_Python_Pyboard_Virtual_Comm_Port_in_FS_Mode_000000000011-if01'
baud = 115200

class pyboardread():  # pragma: no cover
    def __init__(self):
        self.termName = 'nonesofar'
        self.olddict = {}

    def get_name(self):
        return(self.termName)

    def get_temperature(self, format='celsius'):
        mydict = self.get_dict()
        try:
            temp_c = mydict['temperature']
        except:
            temp_c = 0
            
        if format == 'celsius':
            return temp_c
        elif format == 'fahrenheit':
            return temp_c * 1.8 + 32.0
        elif format == 'millicelsius':
            return int(temp_c * 1000)
        else:
            raise ValueError("Unknown format")

    def get_dict(self):

        try:
            serPort = serial.Serial(port=portName,
                                        baudrate=baud,
                                        timeout=0.001,
                                        bytesize=serial.EIGHTBITS,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        xonxoff=False,
                                        rtscts=False,
                                        dsrdtr=False)

        except:
            try:
                
                serPort = serial.Serial(port=altName,
                                        baudrate=baud,
                                        timeout=0.001,
                                        bytesize=serial.EIGHTBITS,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        xonxoff=False,
                                        rtscts=False,
                                        dsrdtr=False)
            except serial.serialutil.SerialException:
                print("Unable to open port '%s'\r" % portName)
                sys.exit(1)
        
        time.sleep(0.3)
        
        # Read the buffer to end
        try:
            r = serPort.read(8)
            response = r
            if len(r) == 0:
                time.sleep(0.5)
                r = serPort.read(8)
                response = r
                
            while len(r) > 0:
                r = serPort.read(8)
                response = response + r
        except:
            print "Failed to read"
        serPort.close()
         
        mydict = None
        # Find the last full json record
        for l in response.splitlines():
            # print '|'+l+'|'
            try:
                mydict = json.loads(l)   
            except:
                pass
        if mydict is None:
            return self.olddict
        else:
            self.olddict = mydict
        return(mydict)
 
if __name__ == '__main__':  # pragma: no cover
    pbr = pyboardread()
    print json.dumps(pbr.get_dict(), sort_keys=True, indent=4)
    print "Temperature is ", pbr.get_temperature('fahrenheit')       
