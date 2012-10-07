#!/usr/bin/python

import pickle
import time
import getpass
import logging
import time
import subprocess
import getopt
import sys
import genctrl
import hotWaterTun
import hoptimer
import hwPump
from x10.controllers.cm11 import CM11


def usage():
    print 'usage:'

simTemp = 70
shutdown = False
controllers = {}
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

if not simulation:
    print "Initializing hardware"
    x10 = CM11('/dev/ttyUSB0')
    x10.open()
    hwTunSwitch = x10.actuator("H14")
    hwPumpSwitch = x10.actuator("I12")

    delayTime = hoptimer.hoptimer()
    mytun = hotWaterTun.hwtHW(hwTunSwitch)
    hwPump = hwPump.hwPump_hw(hwPumpSwitch)
else:
    delayTime = hoptimer.hoptimer_sim()
    mytun = hotWaterTun.hwtsim()
    hwPump = hwPump.hwPump_sim()

controllers['delayTime'] = delayTime
controllers['hotWaterTun'] = mytun
controllers['hwPump'] = hwPump

#currTemp = mytun.temperature()
status = mytun.status()
#watchdog = 0

while True:
    # get data
    try:
        settings = pickle.load(open("/tmp/settings.pkl", "rb"))
    except:
        settings = {
            'temperature': 0,
            'stage': 'stop',
            'name': 'Manual',
            'setTime': 0,
            'setHwVolume': 0
        }

    runStop = settings['runStop']

    # Shut everything down
    if runStop == 'shutdown':
        for key, c in controllers.items():
            del c
        break

    if runStop == 'stop':
        for c in controllers.itervalues():
            c.stop()

    if runStop == 'run':
        for key, c in controllers.items():
            s=settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.start()
                c.update()
            else:
                c.stop()

    # New status dump more in json like format
    stat = {}
    ctrlStat = {}
    for key, c in controllers.items():
        curr = {}
        curr['actual'] = c.get()
        curr['target'] = c.getTarget()
        curr['unit'] = c.getUnit()
        curr['powerOn'] = c.getPowerOn()
        curr['targetMet'] = c.targetMet()
        ctrlStat[key] = curr

    stat['controllers'] = ctrlStat
    stat['runStop'] = runStop
    stat['watchDog'] = int(time.time())
    statout = open('/tmp/status.pkl', 'w')
    # Pickle dictionary using protocol 0.
    pickle.dump(stat, statout)
    statout.close()

    if verbose:
        print "================================"
        print "Target: ", settings
        print "Actual: ", stat
    else:
        sys.stdout.write(".")
        sys.stdout.flush()

    time.sleep(1)
