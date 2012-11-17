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
import appliances.boiler
from x10.controllers.cm11 import CM11


def usage():
    print 'usage:'
    sys.exit


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


def checkHardware(controllers):
    """
    Checks hardware conditions that should be me
    If any is false return false
    Default is true
    """
    hardwareOK = True

    # Hot water pump and wort pump should not be active at the same time
    if controllers['hotWaterPump'].getPowerOn() and \
    controllers['wortPump'].getPowerOn():
        hardwareOK = False
        print "HotWater pump and wort pump on at same time"

    return(hardwareOK)


def runManual(controllers, verbose):
    print "manual"
    while True:
        # get data
        settings = {}
        try:
            settings = pickle.load(open("/tmp/settings.pkl", "rb"))
        except:
            settings['runStop'] = 'stop'
        runStop = settings['runStop']

        # Shut everything down if hardware check shows failure
        if not checkHardware(controllers):
            controllers.shutdown()
            break

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
        if True:
            print ""
            print "Stage: ", r_key
        while not controllers.done():
            controllers.run(settings)

            writeStatus(controllers, settings, r_key, runStop, verbose)
            # Shut everything down if hardware check shows failure
            if not checkHardware(controllers):
                controllers.shutdown()
                break

            time.sleep(1)

if __name__ == "__main__":
    simTemp = 70
    shutdown = False
    controllers = controllers.controllers()
    #sys.exit(0)

    options, remainder = getopt.getopt(sys.argv[1:], 'f:hpsv', [
                         'file',
                         'help',
                         'permissive'
                         'simulate',
                         'verbose',
                         'version=',
                         ])
    verbose = False
    simulation = False
    permissive = False
    recipeFile = ""
    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-f', '--file'):
            recipeFile = arg
        elif opt in ('-p', '--permissive'):
            permissive = True
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
        simX10 = False
        print "Initializing hardware"
        try:
            x10 = CM11('/dev/ttyUSB0')
            x10.open()
            hwTunSwitch = x10.actuator("H14")
            boilerSwitch = x10.actuator("I12")
        except:
            if permissive:
                print "Permissive mode, switch X10 to simulation"
                simX10 = True
            else:
                print "X10 not available"
                sys.exit()

        if simX10:
            controllers.addController('waterHeater',hotWaterTun.hwtsim())
            controllers.addController('boiler', appliances.boiler())
        else:
            controllers.addController('waterHeater',hotWaterTun.hwtHW())
            controllers['waterHeater'].connectSwitch(hwTunSwitch)
            controllers.addController('boiler', appliances.boiler())
            controllers['boiler'].connectSwitch(boilerSwitch)

        try:
            usbPumps = pumpUSB.pumpUSB()
            hotWaterPumpSwitch = usbPumps.getPump(1)
            hwCirculationSwitch = usbPumps.getPump(0)
            wortSwitch = usbPumps.getPump(2)
            mashCirculationSwitch = usbPumps.getPump(3)

        except:
            if permissive:
                print "Permissive mode switching USB to simulation"
                hotWaterPumpSwitch = simswitch.simSwitch()
                hwCirculationSwitch = simswitch.simSwitch()
                wortSwitch = simswitch.simSwitch()
                mashCirculationSwitch = simswitch.simSwitch()
            else:
                raise Exception("USB pumps not available")

        controllers.addController('delayTimer', hoptimer.hoptimer())
        controllers.addController('hotWaterPump',
                    hwPump.hwPump(hotWaterPumpSwitch))
        controllers.addController('waterCirculationPump',
                    circulationPump.circulationPump(hwCirculationSwitch))
        controllers.addController('wortPump', hwPump.hwPump(wortSwitch))
        controllers.addController('mashCirculationPump',
                    circulationPump.circulationPump(mashCirculationSwitch))

    else:
        hotWaterPumpSwitch = simswitch.simSwitch()
        hwCirculationSwitch = simswitch.simSwitch()
        wortSwitch = simswitch.simSwitch()
        mashCirculationSwitch = simswitch.simSwitch()

        controllers.addController('delayTimer', hoptimer.hoptimer())
        controllers.addController('waterHeater', hotWaterTun.hwtsim(None))
        controllers.addController('hotWaterPump',
                    hwPump.hwPump(hotWaterPumpSwitch))
        controllers.addController('waterCirculationPump',
                    circulationPump.circulationPump(hwCirculationSwitch))
        controllers.addController('wortPump', hwPump.hwPump(wortSwitch))
        controllers.addController('mashCirculationPump',
                    circulationPump.circulationPump(mashCirculationSwitch))
        controllers.addController('boiler', appliances.boiler(None))

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
