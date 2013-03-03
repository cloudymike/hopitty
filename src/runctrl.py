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
#import ctrl.controllers
import ctrl.readRecipe
#import ctrl.checkers
import appliances.boiler
#import ctrl.checkers
import switches
import memcache
#@PydevCodeAnalysisIgnore

def usage():
    print 'usage:'
    print "-h: help"
    print "-b file: read beersmith file"
    print "-f file: read JSON file"
    print "-q: quick check"
    print "-v: verbose"
    sys.exit


def writeStatus(controllers, settings, stage, runStop, currentRecipe, verbose):
        ctrlStat = controllers.status()

        stat = {}
        stat['name'] = currentRecipe
        stat['controllers'] = ctrlStat
        stat['runStop'] = runStop
        stat['watchDog'] = int(time.time())
        stat['stage'] = stage

        # If memcache is available, use it
        # ignore error in eclipe on next line
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        mc.set("hopitty_run_key", stat,10)

        #As alternative, save to pickle file
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
        writeStatus(controllers, settings, stage, runStop, 'Manual run', verbose)

        time.sleep(1)


def runRecipe(controllers, recipe, currentRecipe, verbose):
    """
    Goes through all stages of the recipe and runs all controllers
    Reset controllers by stopping them before starting each stage
    """
    runStop = 'run'
    ctrl.stages2Memcache(recipe)
    for r_key, settings in sorted(recipe.items()):
        controllers.stop()
        controllers.run(settings)
        if True:
            print ""
            print "Stage: ", r_key
        while not controllers.done():
            controllers.run(settings)

            writeStatus(controllers, settings, r_key, runStop, currentRecipe, verbose)
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

    # Try to find hw switches
    if not simulation:
        print "Initializing hardware"
        try:
            x10 = switches.myX10('/dev/ttyUSB0')
            x10.open()
        except:
            if permissive:
                print "Permissive mode, switch X10 to simulation"
                x10 = switches.simSwitchList()
                simX10 = True
            else:
                print "X10 not available"
                sys.exit()
                
        try:
            usbPumps = switches.pumpUSB()
        except:
            if permissive:
                print "Permissive mode switching USB to simulation"
                usbPumps = switches.simSwitchList()
            else:
                raise Exception("USB pumps not available")
               
    else:
        x10 = switches.simSwitchList()        
        usbPumps = switches.simSwitchList()
        
    hwTunSwitch = x10.getSwitch("H14")
    boilerSwitch = x10.getSwitch("I12")
    hotWaterPumpSwitch = usbPumps.getSwitch(1)
    hwCirculationSwitch = usbPumps.getSwitch(0)
    wortSwitch = usbPumps.getSwitch(2)
    mashCirculationSwitch = usbPumps.getSwitch(3)

    controllers.addController('waterHeater',appliances.hwt())
    controllers['waterHeater'].connectSwitch(hwTunSwitch)
    controllers.addController('boiler', appliances.boiler())
    controllers['boiler'].connectSwitch(boilerSwitch)
    controllers.addController('delayTimer', appliances.hoptimer())
    controllers.addController('hotWaterPump', appliances.hwPump())
    controllers['hotWaterPump'].connectSwitch(hotWaterPumpSwitch)
    controllers.addController('waterCirculationPump', appliances.circulationPump())
    controllers['waterCirculationPump'].connectSwitch(hwCirculationSwitch)
    controllers.addController('wortPump', appliances.wortPump())
    controllers['wortPump'].connectSwitch(wortSwitch)
    controllers.addController('mashCirculationPump', appliances.circulationPump())
    controllers['mashCirculationPump'].connectSwitch(mashCirculationSwitch)


    # Testing of sensor object Remove me later
    for key, c1 in controllers.items():
        c1.findOrAddSensor(controllers)

    if recipeFile != "":
        data = ctrl.readJson(recipeFile)
        recipe = ctrl.readRecipe(data, controllers)
        recipeName = ctrl.readName(data)
    elif bsmxFile != "":
        data = ctrl.bsmxReadFile(bsmxFile)
        recipe = ctrl.bsmxReadRecipe(data, controllers)
        recipeName = ctrl.bsmxReadName(data)
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
            
            print "===== Running recipe:", recipeName, "====="
            runOK = runRecipe(controllers, recipe, recipeName, verbose)
    if not runOK:
        print "ERROR: Run of controller failed"
        sys.exit(1)
        
    print " "
    print "OK"