#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess

from x10.controllers.cm11 import CM11

# X10 setup. Logger logs to screen
logger = logging.getLogger()
hdlr = logging.StreamHandler() # Console
formatter = logging.Formatter('%(module)s - %(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)
dev = CM11('/dev/ttyUSB0')
dev.open()
livinglamp = dev.actuator("H14")

while True:
    lt=time.localtime(time.time())
    settings=pickle.load(open("settings.pkl","rb"))
    setTemp=int(settings['time'])
    ret=subprocess.check_output('./mytemp')
    currTemp=int(ret)
    print setTemp
    #secs=lt.tm_sec
    me=getpass.getuser()
    if currTemp < setTemp:
        status='On'
        livinglamp.on()
    else:
        status='Off'
        livinglamp.off()
    data1 = {'t': currTemp,
             'me': me,
             'status': status,
             'setSec': setTemp
    }
    print data1
    output = open('data.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(data1, output)
    output.close()
    time.sleep(5)
