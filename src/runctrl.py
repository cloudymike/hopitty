#!/usr/bin/python

# branch t1
import sys
sys.path.append("/home/mikael/workspace/hoppity/src") 
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

import pickle
import time
import getopt
import sys
import appliances
import ctrl
#import appliances.hoptimer
#import appliances.hwt
#import appliances.hwPump
#import appliances.circulationPump
import ctrl.simswitch
import ctrl.controllers
import ctrl.readRecipe
import ctrl.pumpUSB
import ctrl.checkers
import appliances.boiler
from x10.controllers.cm11 import CM11
import ctrl.checkers


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
        if not ctrl.checkers.checkHardware(controllers):
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


def runRecipe(controllers, recipe, verbose):
    """
    Goes through all stages of the recipe and runs all controllers
    Reset controllers by stopping them before starting each stage
    """
    runStop = 'run'
    for r_key, settings in sorted(recipe.items()):
        controllers.stop()
        controllers.run(settings)
        if True:
            print ""
            print "Stage: ", r_key
        while not controllers.done():
            controllers.run(settings)

            writeStatus(controllers, settings, r_key, runStop, verbose)
            # Shut everything down if hardware check shows failure
            if not ctrl.checkHardware(controllers):
                controllers.shutdown()
                return(False)

            time.sleep(1)
    return(True)
            
def quickRecipe(controllers, recipe, verbose):
    """
    Runs through the recipe without any delay to just check it is OK
    This is different from check recipe in that it will also run
    each controller, thus test hardware if connected and not
    permissive
    """
    runStop = 'run'
    for r_key, settings in sorted(recipe.items()):
        controllers.stop()
        controllers.run(settings)
        if True:
            print ""
            print "Stage: ", r_key
        if not ctrl.checkHardware(controllers):
            controllers.shutdown()
            return(False)
#            time.sleep(1)
    return(True)

if __name__ == "__main__":
    simTemp = 70
    shutdown = False
    controllers = ctrl.controllerList()
    options, remainder = getopt.getopt(sys.argv[1:], 'b:f:hqv', [
                         'bsmx=',
                         'file=',
                         'help',
                         'quick',
                         'verbose',
                         'version=',
                         ])
    verbose = False
    simulation = False
    permissive = True
    quick = False
    recipeFile = ""
    bsmxFile = ""
    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-f', '--file'):
            recipeFile = arg
        if opt in ('-b', '--bsmx'):
            bsmxFile = arg
        elif opt in ('-q', '--quick'):
            quick = True
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt == '--version':
            version = arg

    if verbose:
        print 'Verbose'
        print "bsmxFile:", bsmxFile

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
            controllers.addController('waterHeater',appliances.hwt())
            controllers.addController('boiler', appliances.boiler())
        else:
            controllers.addController('waterHeater',appliances.hwt())
            controllers['waterHeater'].connectSwitch(hwTunSwitch)
            controllers.addController('boiler', appliances.boiler())
            controllers['boiler'].connectSwitch(boilerSwitch)

        try:
            usbPumps = ctrl.pumpUSB()
            hotWaterPumpSwitch = usbPumps.getPump(1)
            hwCirculationSwitch = usbPumps.getPump(0)
            wortSwitch = usbPumps.getPump(2)
            mashCirculationSwitch = usbPumps.getPump(3)

        except:
            if permissive:
                print "Permissive mode switching USB to simulation"
                hotWaterPumpSwitch = ctrl.simswitch.simSwitch()
                hwCirculationSwitch = ctrl.simswitch.simSwitch()
                wortSwitch = ctrl.simswitch.simSwitch()
                mashCirculationSwitch = ctrl.simswitch.simSwitch()
            else:
                raise Exception("USB pumps not available")

        controllers.addController('delayTimer', appliances.hoptimer())
        controllers.addController('hotWaterPump', appliances.hwPump())
        controllers['hotWaterPump'].connectSwitch(hotWaterPumpSwitch)
        controllers.addController('waterCirculationPump', appliances.circulationPump())
        controllers['waterCirculationPump'].connectSwitch(hwCirculationSwitch)
        controllers.addController('wortPump', appliances.wortPump())
        controllers['wortPump'].connectSwitch(wortSwitch)
        controllers.addController('mashCirculationPump', appliances.circulationPump())
        controllers['mashCirculationPump'].connectSwitch(mashCirculationSwitch)

    else:
        hotWaterPumpSwitch = ctrl.simSwitch()
        hwCirculationSwitch = ctrl.simSwitch()
        wortSwitch = ctrl.simSwitch()
        mashCirculationSwitch = ctrl.simSwitch()

        controllers.addController('delayTimer', appliances.hoptimer())
        controllers.addController('waterHeater', appliances.hwt())
        controllers.addController('hotWaterPump',
                    appliances.hwPump(hotWaterPumpSwitch))
        controllers.addController('waterCirculationPump',
                    appliances.circulationPump(hwCirculationSwitch))
        controllers.addController('wortPump', appliances.wortPump(wortSwitch))
        controllers.addController('mashCirculationPump',
                    appliances.circulationPump(mashCirculationSwitch))
        controllers.addController('boiler', appliances.boiler())
        
    # Testing of sensor object Remove me later
    for key, c1 in controllers.items():
        c1.findOrAddSensor(controllers)

    if recipeFile != "":
        recipe = ctrl.readRecipe(recipeFile, controllers)
    elif bsmxFile != "":
        recipe = ctrl.bsmxReadRecipe(bsmxFile, controllers)
    else:   
        recipe = {}
    if verbose:
        ctrl.prettyPrintStages(recipe)

    if recipe == {}:
        runManual(controllers, verbose)
        runOK = True
    else:
        if not ctrl.checkers.checkRecipe(controllers, recipe, verbose):
            print "ERROR: Recipe check failed"
            sys.exit(1)
            
        if quick:
            print "Quick run"
            runOK = quickRecipe(controllers, recipe, verbose)
        else:
            print "Running recipe"
            runOK = runRecipe(controllers, recipe, verbose)
    if not runOK:
        print "ERROR: Run of controller failed"
        sys.exit(1)
        
    print " "
    print "OK"