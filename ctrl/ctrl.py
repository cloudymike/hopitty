#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess
import getopt
import sys
import hotWaterTun

simTemp=70

#sys.exit(0)

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
    mytun=hotWaterTun.hwtHW()
else:
    mytun=hotWaterTun.hwtsim()
    
currTemp = mytun.temperature()
status = mytun.status()

while True:
    settings=pickle.load(open("/tmp/settings.pkl","rb"))
    setTemp=int(settings['temperature'])
    currTemp = mytun.temperature()
    #lt=time.localtime(time.time())
    #secs=lt.tm_sec
    me=getpass.getuser()
    mytun.thermostat()
    status = mytun.status()
    data1 = {'t': currTemp,
             'me': me,
             'status': status,
             'setTemp': setTemp
    }
    print data1
    output = open('/tmp/data.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(data1, output)
    output.close()
    time.sleep(1)
