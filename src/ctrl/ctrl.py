#!/usr/bin/python

import time
import pickle
import getopt
import sys
import hotWaterTun
import hoptimer
import hwPump
import controllers
import readRecipe
from x10.controllers.cm11 import CM11


def usage():
    print 'usage:'


def writeStatus(controllers, settings, stage, runStop, verbose):
        ctrlStat = controllers.status()

        stat = {}
        stat['controllers'] = ctrlStat
        stat['runStop'] = runStop
        stat['watchDog'] = int(time.time())
        stat['stage'] = stage
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


def runManual(controllers, verbose):
    settings = {}
    while True:
        # get data
        try:
            settings = pickle.load(open("/tmp/settings.pkl", "rb"))
        except:
            settings['runStop'] = 'stop'
        runStop = settings['runStop']

        # Shut everything down
        if runStop == 'shutdown':
            controllers.shutdown()
            break

        if runStop == 'stop':
            controllers.stop()

        if runStop == 'run':
            controllers.run(settings)

        stage = 'Manual'
        writeStatus(controllers, settings, stage, runStop, verbose)

        time.sleep(1)


def runRecipe(controllers, recipe, verbose):
    runStop = 'run'
    for r_key, settings in sorted(recipe.items()):
        controllers.run(settings)
        while not controllers.done():
            controllers.run(settings)
            if verbose:
                print "================================"
                print "Stage: ", r_key

            writeStatus(controllers, settings, r_key, runStop, verbose)
            time.sleep(1)

if __name__ == "__main__":
    simTemp = 70
    shutdown = False
    controllers = controllers.controllers()
    #sys.exit(0)

    options, remainder = getopt.getopt(sys.argv[1:], 'f:hsv', [
                         'file',
                         'help',
                         'simulate',
                         'verbose',
                         'version=',
                         ])
    verbose = False
    simulation = False
    file = ""
    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-f', '--file'):
            file = arg
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
        mytun = hotWaterTun.hwtsim(None)
        hwPump = hwPump.hwPump_sim()

    controllers.addController(delayTime)
    controllers.addController(mytun)
    controllers.addController(hwPump)

    status = mytun.status()

    if file != "":
        recipe = readRecipe.readRecipe(file, controllers)
    else:
        recipe = {}
    if verbose:
        print recipe

    if recipe == {}:
        runManual(controllers, verbose)
    else:
        runRecipe(controllers, recipe, verbose)
