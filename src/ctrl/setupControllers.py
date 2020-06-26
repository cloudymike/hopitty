
import time
import datetime
import ctrl
import recipeReader
import appliances.boiler
import switches
import sensors
import sys
import logging
import equipment.allEquipment


def setupControllers(verbose, simulation, permissive, equipment):
    controllers = ctrl.controllerList()
    # The controllerinfo is a special snowflake that stores some extra global controller info
    # It does not do anything intelligent itherwise and will always meet target
    controllers.addController('controllerInfo', appliances.controllerinfo())
    
    if equipment is None:
        logging.error('Equipment is None')
        return(None)
    controllers['controllerInfo'].setEquipment(equipment)

    # Timer is always required in all equipment
    controllers.addController('delayTimer', appliances.hoptimer())

    print "Try to find hw switches"
    if not simulation:
        logging.info("Initializing hardware")
        try:
            usbPumps = switches.pumpUSB()
        except:
            if permissive:
                logging.info("**********USB pumps not found, simulating HW")
                usbPumps = switches.simSwitchList()
            else:
                raise Exception("USB pumps not available")
    else:
        usbPumps = switches.simSwitchList()

    tempSensors = sensors.tempSensorDict()

    print("Setting up appliances")

    hwTunSwitch = switches.powerSwitch(1)
    boilerSwitch = switches.powerSwitch(2)
    aeratorSwitch = switches.air8800Switch()
    coolerSwitch = switches.coolerSwitch()
    mashStirSwitch = switches.mashStirSwitch()
    #mashStirSwitch = switches.mashStir8800Switch()
    boilerValveSwitch = switches.boilerValveSwitch()
    hotWaterPumpSwitch = usbPumps.getSwitch(1)
    hwCirculationSwitch = usbPumps.getSwitch(0)
    wortSwitch = usbPumps.getSwitch(2)
    mashCirculationSwitch = usbPumps.getSwitch(3)
    controllers.addController('waterHeater', appliances.hwt())
    controllers['waterHeater'].connectSwitch(hwTunSwitch)
    controllers['waterHeater'].connectSensor(tempSensors.getSensor('281a7a6d0b000096'))

    controllers.addController('boiler', appliances.boiler())
    controllers['boiler'].connectSwitch(boilerSwitch)
    boilerSensor = tempSensors.getSensor('28ff922d0116039e')
    controllers['boiler'].connectSensor(boilerSensor)

    controllers.addController('aerator', appliances.aerator())
    controllers['aerator'].connectSwitch(aeratorSwitch)

    controllers.addController('cooler', appliances.cooler())
    # Do not use coolerswitch anymore, that one is now on plate chiller
    #controllers['cooler'].connectSwitch(coolerSwitch)
    controllers['cooler'].connectSensor(boilerSensor)

    # Reuse of same switch for plate cooler as immersion cooler
    controllers.addController('plateValve', appliances.plateValve())
    controllers['plateValve'].connectSwitch(coolerSwitch)

    controllers.addController('mashStirrer', appliances.mashStirrer())
    controllers['mashStirrer'].connectSwitch(mashStirSwitch)

    if 'mashHeater' in equipment['componentlist']:
        controllers.addController('mashHeater', appliances.mashHeater())
        controllers['mashHeater'].connectSwitch(mashCirculationSwitch)
        controllers['mashHeater'].connectSensor(tempSensors.getSensor('28ffa570021603ea'))
    elif 'mashTemp' in equipment['componentlist']:
        controllers.addController('mashTemp', appliances.mashHeater())
        controllers['mashTemp'].connectSwitch(mashCirculationSwitch)
        controllers['mashTemp'].connectSensor(tempSensors.getSensor('28ffa570021603ea'))

    controllers.addController('boilerValve', appliances.boilerValve())
    controllers['boilerValve'].connectSwitch(boilerValveSwitch)
    controllers.addController('hotWaterPump', appliances.hwPump())
    controllers['hotWaterPump'].connectSwitch(hotWaterPumpSwitch)

    if 'hwtVolume' in equipment['componentlist']:
        controllers.addController('hwtVolume', appliances.hwtVolume())
        controllers['hwtVolume'].attachHost(controllers['hotWaterPump'])
        controllers['hwtVolume'].setMaxVol(equipment['specs']['hwtVolumeMax'])

    controllers.addController('waterCirculationPump',
                              appliances.circulationPump())
    controllers['waterCirculationPump'].connectSwitch(hwCirculationSwitch)
    controllers.addController('wortPump', appliances.wortPump())
    controllers['wortPump'].connectSwitch(wortSwitch)

    if 'hwtVolume' in equipment['componentlist']:
        controllers.addController('boilerVolume', appliances.boilerVolume())
        controllers['boilerVolume'].attachHost(controllers['wortPump'])

    if 'dispenser' in equipment['componentlist']:
        controllers.addController('dispenser1', appliances.dispenser(1))
        controllers.addController('dispenser2', appliances.dispenser(2))
        controllers.addController('dispenser3', appliances.dispenser(3))
        controllers.addController('dispenser4', appliances.dispenser(4))
    
    controllers.addController('envTemp', appliances.envTemp())
    controllers['envTemp'].connectSensor(tempSensors.getSensor('28ffa570021603ea'))
    #controllers['envTemp'].connectSensor(sensors.envTempSensor())

    print("appliance setup done")
    # Testing of sensor object Remove me later
    for key, c1 in controllers.items():
        c1.findOrAddSensor(controllers)
        # print key
    "returning..."
    return(controllers)

