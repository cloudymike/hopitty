
import pickle
import time
import datetime
import ctrl.readRecipe
import appliances.boiler
import switches
import sys
import dataMemcache


def quickRecipe(controllers, recipe, verbose):
    """
    Runs through the recipe without any delay to just check it is OK
    This is different from check recipe in that it will also run
    each controller, thus test hardware if connected and not
    permissive
    """
    controllers.stop()
    for r_key, settings in sorted(recipe.items()):
        startTime = datetime.datetime.now()
        controllers.run(settings)
        if True:
            print ""
            print "Stage: ", r_key
        if not ctrl.checkHardware(controllers):
            controllers.shutdown()
            return(False)
        controllers.stopCurrent(settings)
        if verbose:
            delta = datetime.datetime.now() - startTime
            print "  Exectime: ", delta.microseconds, "uS"
    return(True)


def setupControllers(verbose, simulation, permissive):
    controllers = ctrl.controllerList()
    # Try to find hw switches
    if not simulation:
        print "Initializing hardware"
        try:
            x10 = switches.myX10('/dev/serial/by-id/usb-Prolific_Technology'
                                 '_Inc._USB-Serial_Controller-if00-port0')
            x10.open()
        except:
            if permissive:
                print "**********X10 not found, simulating HW"
                x10 = switches.simSwitchList()
                simX10 = True
            else:
                print "X10 not available"
                sys.exit()

        try:
            usbPumps = switches.pumpUSB()
        except:
            if permissive:
                print "**********USB pumps not found, simulating HW"
                usbPumps = switches.simSwitchList()
            else:
                raise Exception("USB pumps not available")
    else:
        x10 = switches.simSwitchList()
        usbPumps = switches.simSwitchList()

    print "Setting up appliances"
    hwTunSwitch = x10.getSwitch("H14")
    boilerSwitch = x10.getSwitch("I12")
    # aeratorSwitch = x10.getSwitch("H10")
    aeratorSwitch = switches.simSwitch()
    coolerSwitch = switches.coolerSwitch()
    mashStirSwitch = switches.mashStirSwitch()
    boilerValveSwitch = switches.boilerValveSwitch()
    hotWaterPumpSwitch = usbPumps.getSwitch(1)
    hwCirculationSwitch = usbPumps.getSwitch(0)
    wortSwitch = usbPumps.getSwitch(2)
    # mashCirculationSwitch = usbPumps.getSwitch(3)

    controllers.addController('waterHeater', appliances.hwt())
    controllers['waterHeater'].connectSwitch(hwTunSwitch)
    controllers['waterHeater'].setx(x10)

    controllers.addController('boiler', appliances.boiler())
    controllers['boiler'].connectSwitch(boilerSwitch)
    controllers['boiler'].setx(x10)

    controllers.addController('aerator', appliances.aerator())
    controllers['aerator'].connectSwitch(aeratorSwitch)

    controllers.addController('cooler', appliances.cooler())
    controllers['cooler'].connectSwitch(coolerSwitch)
    boilerSensor = controllers['boiler'].getSensor()
    controllers['cooler'].connectSensor(boilerSensor)
    controllers.addController('mashStirrer', appliances.mashStirrer())
    controllers['mashStirrer'].connectSwitch(mashStirSwitch)
    controllers.addController('boilerValve', appliances.boilerValve())
    controllers['boilerValve'].connectSwitch(boilerValveSwitch)
    controllers.addController('delayTimer', appliances.hoptimer())
    controllers.addController('hotWaterPump', appliances.hwPump())
    controllers['hotWaterPump'].connectSwitch(hotWaterPumpSwitch)
    controllers.addController('waterCirculationPump',
                              appliances.circulationPump())
    controllers['waterCirculationPump'].connectSwitch(hwCirculationSwitch)
    controllers.addController('wortPump', appliances.wortPump())
    controllers['wortPump'].connectSwitch(wortSwitch)
    # controllers.addController('mashCirculationPump', \
    #                          appliances.circulationPump())
    # controllers['mashCirculationPump'].connectSwitch(mashCirculationSwitch)
    controllers.addController('dispenser1', appliances.dispenser(1))
    controllers.addController('dispenser2', appliances.dispenser(2))
    controllers.addController('dispenser3', appliances.dispenser(3))
    controllers.addController('dispenser4', appliances.dispenser(4))

    print "appliance setup done"
    # Testing of sensor object Remove me later
    for key, c1 in controllers.items():
        c1.findOrAddSensor(controllers)
        # print key
    "returning..."
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
        self.controllers = setupControllers(self.verbose, self.simulation,
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

    def stagesIn(self, stages):
        self.recipeName = 'manualStages'
        self.stages = stages

    def getStages(self):
        return(self.stages)

    def getRecipeName(self):
        return(self.recipeName)

    def getControllers(self):
        return(self.controllers)

    def run(self):
        if self.check():
            runOK = self.runRecipe()
            # (self.controllers, self.stages, self.recipeName, self.verbose)
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
        return(ctrl.checkers.checkRecipe(self.controllers, self.stages,
                                         self.verbose))

    def checkBSMX(self, xml):
        """Checks the BSMX recipe against controllers without loading it"""
        if not ctrl.checkVolBSMX(xml):
            return(False)
        stages = ctrl.bsmxReadRecipe(xml, self.controllers)
        if stages is not None:
            return(ctrl.checkers.checkRecipe(self.controllers, stages,
                                             self.verbose))
        else:
            return(False)

    def runRecipe(self):
    # controllers, recipe, currentRecipe, verbose):
        """
        Goes through all stages of the recipe and runs all controllers
        Reset controllers by stopping them before starting each stage
        """
        myData = dataMemcache.brewData()
        myData.setStagesList(self.stages)
        # Make sure skip is not accidentally pressed
        myData.setSkip(False)
        myData.setPause(False)
        myData.unsetError()

        for r_key, settings in sorted(self.stages.items()):
            if myData.getCtrlRunning():
                self.runStage(r_key, settings)
        self.controllers.stop()
        return(True)

    def runStage(self, r_key, settings):
        myData = dataMemcache.brewData()

        self.controllers.stop()
        self.controllers.run(settings)
        if True:
            print ""
            print "Stage: ", r_key
        while ((not self.controllers.done()) and
              (myData.getCtrlRunning()) and
              (not myData.getSkip())) or myData.getPause():

            startTime = datetime.datetime.now()
            if myData.getPause():
                self.controllers.pause(settings)
            else:
                self.controllers.run(settings)

            self.writeStatus(settings, r_key)
            # Shut everything down if hardware check shows failure
            if not ctrl.checkHardware(self.controllers):
                self.controllers.shutdown()
                print '>>>>>>>>>>>>>>HW Fail<<<<<<<<<<<<<<<<<'
                return(False)
            if self.verbose:
                delta = datetime.datetime.now() - startTime
                print "  Exectime: ", delta.microseconds, "uS"
            time.sleep(1)
        myData.setSkip(False)

    def HWOK(self):
        return(self.controllers.HWOK())

    def writeStatus(self, settings, stage):
            ctrlStat = self.controllers.status()
            myData = dataMemcache.brewData()

            stat = {}
            stat['name'] = self.recipeName
            stat['controllers'] = ctrlStat

            myData.setCurrentStage(stage)
            myData.resetWatchdog()
            myData.setStatus(stat)

            if myData.getError():
                crumb = 'E'
            elif myData.getPause():
                crumb = 'P'
            else:
                crumb = '.'

            if self.verbose:
                print "================================"
                print "Target: ", settings
                print "Actual: ", stat
            else:
                sys.stdout.write(crumb)
                sys.stdout.flush()
