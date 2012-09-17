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
import hoptimer


def usage():
    print 'usage:'

simTemp = 70
shutdown = False
#sys.exit(0)

options, remainder = getopt.getopt(sys.argv[1:], 'hsv', [
                                                         'help',
                                                         'simulate',
                                                         'verbose',
                                                         'version=',
                                                        ])
verbose = False
simulation = False
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

# Initially for debugging
#lt=time.localtime(time.time())
#secs=lt.tm_sec
me = getpass.getuser()

starttime=hoptimer.hoptimer()
starttime.set(9999)

# X10 setup. Logger logs to screen
if not simulation:
    mytun = hotWaterTun.hwtHW()
else:
    mytun = hotWaterTun.hwtsim()

currTemp = mytun.temperature()
status = mytun.status()
watchdog = 0

while True:
    # get data
    settings = pickle.load(open("/tmp/settings.pkl", "rb"))
    stage = settings['stage']

    if stage == 'shutdown':
        del mytun
        break

    if stage == 'stop':
        mytun.stop()

    if stage == 'run':
        # process
        mytun.setTemp(int(settings['temperature']))
        mytun.thermostat()

    # Thins to always do
    currTemp = mytun.temperature()

    watchdog=int(time.time())
    # Save data
    status = mytun.status()
    data1 = {'t': currTemp,
             'me': me,
             'watchdog':watchdog,
             'status': status,
             'setTemp': int(settings['temperature']),
             'starttime': starttime.get()
    }
    print data1
    output = open('/tmp/data.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(data1, output)
    output.close()
    time.sleep(1)
