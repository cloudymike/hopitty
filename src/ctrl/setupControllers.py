
import time
import datetime
import ctrl
import recipeReader
import appliances.boiler
import switches
import sys
import logging


def setupControllers(verbose, simulation, permissive):
    controllers = ctrl.controllerList()
    print "Try to find hw switches"
    if not simulation:
        logging.info("Initializing hardware")
        x10 = None
        try:
            usbPumps = switches.pumpUSB()
        except:
            if permissive:
                logging.info("**********USB pumps not found, simulating HW")
                usbPumps = switches.simSwitchList()
            else:
                raise Exception("USB pumps not available")
    else:
        x10 = switches.simSwitchList()
        usbPumps = switches.simSwitchList()

    print("Setting up appliances")

    hwTunSwitch = switches.powerSwitch(1)
    boilerSwitch = switches.powerSwitch(2)
    print 0
    aeratorSwitch = switches.air8800Switch()
    print 0.2
    coolerSwitch = switches.coolerSwitch()
    mashStirSwitch = switches.mashStirSwitch()
    #mashStirSwitch = switches.mashStir8800Switch()
    print 0.5
    boilerValveSwitch = switches.boilerValveSwitch()
    hotWaterPumpSwitch = usbPumps.getSwitch(1)
    hwCirculationSwitch = usbPumps.getSwitch(0)
    wortSwitch = usbPumps.getSwitch(2)
    # mashCirculationSwitch = usbPumps.getSwitch(3)
    print 1
    controllers.addController('waterHeater', appliances.hwt())
    controllers['waterHeater'].connectSwitch(hwTunSwitch)
    controllers['waterHeater'].setx(x10)

    controllers.addController('boiler', appliances.boiler())
    controllers['boiler'].connectSwitch(boilerSwitch)
    controllers['boiler'].setx(x10)

    controllers.addController('aerator', appliances.aerator())
    controllers['aerator'].connectSwitch(aeratorSwitch)
    print 2
    controllers.addController('cooler', appliances.cooler())
    controllers['cooler'].connectSwitch(coolerSwitch)
    boilerSensor = controllers['boiler'].getSensor()
    controllers['cooler'].connectSensor(boilerSensor)

    # Reuse of same switch for plate cooler as immersion cooler
    controllers.addController('plateValve', appliances.plateValve())
    controllers['plateValve'].connectSwitch(coolerSwitch)

    controllers.addController('mashStirrer', appliances.mashStirrer())
    controllers['mashStirrer'].connectSwitch(mashStirSwitch)
    controllers.addController('mashHeater', appliances.mashHeater())
    print 5
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
    controllers.addController('boilerVolume', appliances.boilerVolume())
    controllers['boilerVolume'].attachHost(controllers['wortPump'])
    # controllers.addController('mashCirculationPump', \
    #                          appliances.circulationPump())
    # controllers['mashCirculationPump'].connectSwitch(mashCirculationSwitch)
    controllers.addController('dispenser1', appliances.dispenser(1))
    controllers.addController('dispenser2', appliances.dispenser(2))
    controllers.addController('dispenser3', appliances.dispenser(3))
    controllers.addController('dispenser4', appliances.dispenser(4))
    
    controllers.addController('envTemp', appliances.mashHeater())

    print("appliance setup done")
    # Testing of sensor object Remove me later
    for key, c1 in controllers.items():
        c1.findOrAddSensor(controllers)
        # print key
    "returning..."
    return(controllers)
