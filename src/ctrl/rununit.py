#!/usr/bin/python

import pickle
import time
import ctrl.readRecipe
import appliances.boiler
import switches
import sys
import dataMemcache


def writeStatus(controllers, settings, stage, runStop, currentRecipe, verbose):
        ctrlStat = controllers.status()
        myData = dataMemcache.brewData()

        stat = {}
        stat['name'] = currentRecipe
        stat['controllers'] = ctrlStat
        stat['runStop'] = runStop
        stat['watchDog'] = int(time.time())
        stat['stage'] = stage

        myData.setStatus(stat)

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
        writeStatus(controllers, settings, stage, runStop, 'Manual run', \
                    verbose)

        time.sleep(1)


def runRecipe(controllers, recipe, currentRecipe, verbose):
    """
    Goes through all stages of the recipe and runs all controllers
    Reset controllers by stopping them before starting each stage
    """
    runStop = 'run'
    myData = dataMemcache.brewData()
    myData.setStagesList(recipe)
    for r_key, settings in sorted(recipe.items()):
        controllers.stop()
        controllers.run(settings)
        if True:
            print ""
            print "Stage: ", r_key
        while not controllers.done():
            controllers.run(settings)

            writeStatus(controllers, settings, r_key, runStop, currentRecipe, \
                        verbose)
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


def setupControllers(verbose, simulation, permissive):
    controllers = ctrl.controllerList()
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

    controllers.addController('waterHeater', appliances.hwt())
    controllers['waterHeater'].connectSwitch(hwTunSwitch)
    controllers.addController('boiler', appliances.boiler())
    controllers['boiler'].connectSwitch(boilerSwitch)
    controllers.addController('delayTimer', appliances.hoptimer())
    controllers.addController('hotWaterPump', appliances.hwPump())
    controllers['hotWaterPump'].connectSwitch(hotWaterPumpSwitch)
    controllers.addController('waterCirculationPump', \
                              appliances.circulationPump())
    controllers['waterCirculationPump'].connectSwitch(hwCirculationSwitch)
    controllers.addController('wortPump', appliances.wortPump())
    controllers['wortPump'].connectSwitch(wortSwitch)
    controllers.addController('mashCirculationPump', \
                              appliances.circulationPump())
    controllers['mashCirculationPump'].connectSwitch(mashCirculationSwitch)
    controllers.addController('dispenser1', appliances.dispenser(1))
    controllers.addController('dispenser2', appliances.dispenser(2))
    controllers.addController('dispenser3', appliances.dispenser(3))
    controllers.addController('dispenser4', appliances.dispenser(4))

    # Testing of sensor object Remove me later
    for key, c1 in controllers.items():
        c1.findOrAddSensor(controllers)
        print key
    return(controllers)


def getRecipeName(jsonFile, bsmxFile):
    if jsonFile != "":
        data = ctrl.readJson(jsonFile)
        return(ctrl.readName(data))
    elif bsmxFile != "":
        data = ctrl.bsmxReadFile(bsmxFile)
        return(ctrl.bsmxReadName(data))
    else:
        return('Manual')


def getStages(jsonFile, bsmxFile, controllers):
    if jsonFile != "":
        data = ctrl.readJson(jsonFile)
        stages = ctrl.readRecipe(data, controllers)
    elif bsmxFile != "":
        data = ctrl.bsmxReadFile(bsmxFile)
        stages = ctrl.bsmxReadRecipe(data, controllers)
    else:
        stages = {}
    return(stages)


class rununit():
    """
    This class will wrap all of the other classes required
    to do a mash run
    """

    def __init__(self):
        self.verbose = False
        self.simulation = False
        self.permissive = True
        self.controllers = setupControllers(self.verbose, self.simulation, \
                                            self.permissive)
        self.recipeName = ""
        self.stages = {}

    def __del__(self):
        self.controllers.shutdown()

    def bsmxIn(self, xml):
        """Inputs data from a bsmx doc string"""
        print "==================bsmx"
        self.recipeName = ctrl.bsmxReadName(xml)
        self.stages = ctrl.bsmxReadRecipe(xml, self.controllers)

    def jsonIn(self, json):
        self.recipeName = ctrl.readName(json)
        self.stages = ctrl.readRecipe(json, self.controllers)

    def getStages(self):
        return(self.stages)

    def run(self):
        if self.check():
            runOK = runRecipe(self.controllers, self.stages, \
                          self.recipeName, self.verbose)
            return(runOK)
        else:
            return(False)

    def stop(self):
        self.controllers.stop()

    def quick(self):
        if self.check():
            runOK = quickRecipe(self.controllers, self.stages, self.verbose)
            return(runOK)
        else:
            return(False)

    def check(self):
        return(ctrl.checkers.checkRecipe(self.controllers, self.stages, \
                                         self.verbose))

    def checkBSMX(self, xml):
        """Checks the BSMX recipe against controllers without loading it"""
        if not ctrl.checkVolBSMX(xml):
            return(False)
        stages = ctrl.bsmxReadRecipe(xml, self.controllers)
        if stages != None:
            return(ctrl.checkers.checkRecipe(self.controllers, stages, \
                                         self.verbose))
        else:
            return(False)
