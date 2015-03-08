
import time
import datetime
import ctrl
import recipeReader
import appliances.boiler
import switches
import sys


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
                #simX10 = True
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
    aeratorSwitch = x10.getSwitch("G10")
    #aeratorSwitch = switches.simSwitch()
    coolerSwitch = switches.coolerSwitch()
    #mashStirSwitch = switches.mashStirSwitch()
    mashStirSwitch = switches.mashStir8800Switch()
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
