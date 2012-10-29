#!/usr/bin/python

# branch t1

import pickle
import time
import getopt
import sys
import simswitch
import hotWaterTun
import hoptimer
import hwPump
import circulationPump
import controllers
import readRecipe
import pumpUSB
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
    while True:
        # get data
        settings = {}
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

def checkRecipe(controllers, recipe, verbose):
    """
    Go through all the stages in the recipe and see
    that the controllers match the controllers available
    """
    for r_key, settings in sorted(recipe.items()):
        controllers.check(settings)

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
    recipeFile = ""
    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-f', '--file'):
            recipeFile = arg
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
        boilerSwitch = x10.actuator("I12")
        
        usbPumps = pumpUSB.pumpUSB()
        hotWaterPumpSwitch = pumpUSB.pumpUSB(usbPumps, 0)
        hwCirculationSwitch = pumpUSB.pumpUSB(usbPumps, 1)
        wortSwitch = pumpUSB.pumpUSB(usbPumps, 2)
        mashCirculationSwitch = pumpUSB.pumpUSB(usbPumps, 3)

        controllers.addController('delayTimer', hoptimer.hoptimer())
        controllers.addController('waterHeater', hotWaterTun.hwtHW(hwTunSwitch))
        controllers.addController('hotWaterPump', hwPump.hwPump(hotWaterPumpSwitch))
        controllers.addController('waterCirculationPump', circulationPump.circulationPump(hwCirculationSwitch))
        controllers.addController('wortPump', hwPump.hwPump(wortSwitch))
        controllers.addController('mashCirculationPump', circulationPump.circulationPump(mashCirculationSwitch))
        
        
    else:
        hotWaterPumpSwitch = simswitch.simSwitch()
        hwCirculationSwitch = simswitch.simSwitch()
        wortSwitch = simswitch.simSwitch()
        mashCirculationSwitch = simswitch.simSwitch()

        controllers.addController('delayTimer', hoptimer.hoptimer_sim())
        controllers.addController('waterHeater', hotWaterTun.hwtsim(None))
        controllers.addController('hotWaterPump', hwPump.hwPump(hotWaterPumpSwitch))
        controllers.addController('waterCirculationPump', 
                                  circulationPump.circulationPump(hwCirculationSwitch))
        controllers.addController('wortPump', hwPump.hwPump(wortSwitch))
        controllers.addController('mashCirculationPump', 
                                  circulationPump.circulationPump(mashCirculationSwitch))
 
    if recipeFile != "":
        recipe = readRecipe.readRecipe(recipeFile, controllers)
    else:
        recipe = {}
    if verbose:
        print recipe

    if recipe == {}:
        runManual(controllers, verbose)
    else:
        checkRecipe(controllers, recipe, verbose)
        runRecipe(controllers, recipe, verbose)
