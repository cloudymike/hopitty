#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess
import getopt
import sys

from x10.controllers.cm11 import CM11

def usage():
   print 'usage:'

options, remainder = getopt.getopt(sys.argv[1:], 'hsv', [
                                                         'help',
                                                         'simulate',
                                                         'verbose',
                                                         'version=',
                                                        ])
verbose=False
simulation=False
for opt, arg in options:
    if opt in ('-h', '--help'):
        usage()
    elif opt in ('-s', '--simulate'):
        simulation = True
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt == '--version':
        version = arg

if verbose:
    print 'Verbose'
    if simulation:
        print 'Simulation mode'

# X10 setup. Logger logs to screen
if not simulation:
    logger = logging.getLogger()
    hdlr = logging.StreamHandler() # Console
    formatter = logging.Formatter('%(module)s - %(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)
    dev = CM11('/dev/ttyUSB0')
    dev.open()
    hotWaterTun = dev.actuator("H14")

while True:
    lt=time.localtime(time.time())
    settings=pickle.load(open("../datadir/settings.pkl","rb"))
    setTemp=int(settings['t'])
    ret=subprocess.check_output('./mytemp')
    if not simulation:
        currTemp=int(ret)
    else:
        currTemp=123
    print setTemp
    #secs=lt.tm_sec
    me=getpass.getuser()
    if currTemp < setTemp:
        status='On'
        if not simulation:
            hotWaterTun.on()
    else:
        status='Off'
        if not simulation:
            hotWaterTun.off()
    data1 = {'t': currTemp,
             'me': me,
             'status': status,
             'setSec': setTemp
    }
    print data1
    output = open('../datadir/data.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(data1, output)
    output.close()
    time.sleep(5)
