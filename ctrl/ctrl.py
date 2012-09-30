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

    delayTime=hoptimer.hoptimer()
    mytun = hotWaterTun.hwtHW(hwTunSwitch)
    hwPump = hwPump.hwPump_hw(hwPumpSwitch)
else:
    delayTime=hoptimer.hoptimer_sim()
    mytun = hotWaterTun.hwtsim()
    hwPump = hwPump.hwPump_sim()

#currTemp = mytun.temperature()
status = mytun.status()
#watchdog = 0

while True:
    # get data
    settings = pickle.load(open("/tmp/settings.pkl", "rb"))
    stage = settings['stage']

    if stage == 'shutdown':
        del mytun
        break

# Shut everything down
    if stage == 'stop':
        mytun.stop()
        delayTime.stop()

    if stage == 'run':
        # process
        mytun.setTemp(int(settings['temperature']))
        mytun.update()
        delayTime.set(int(settings['setTime']))
        delayTime.update()
        hwPump.set(float(settings['setHwVolume']))
        hwPump.update()

    data1 = {'t': mytun.get(),
             'me': me,
             'watchdog':int(time.time()),
             'status': mytun.status(),
             'delayTime': delayTime.get(),
             'hwtDone': mytun.targetMet(),
             'delayTimeDone': delayTime.targetMet(),
             'hwPumpVolume' : hwPump.get(),
             'hwPumpDone' : hwPump.targetMet(),
    }
    if verbose:
        print "================================"
        print "Target: ", settings
        print "Actual: ", data1
    else:
        sys.stdout.write(".")
        sys.stdout.flush()

    output = open('/tmp/data.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(data1, output)
    output.close()
    time.sleep(1)
