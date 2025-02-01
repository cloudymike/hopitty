
import time
import datetime
import ctrl.controllers
import recipeReader

import appliances.boiler
import appliances.controllerinfo
import appliances.hoptimer
import appliances.hotWaterTun
import appliances.aerator
import appliances.cooler
import appliances.plateValve
import appliances.mashStirrer
import appliances.mashHeater
import appliances.boilerValve
import appliances.hwPump
import appliances.hwtVolume
import appliances.mashVolume
import appliances.circulationPump
import appliances.boilerVolume
import appliances.dispenser
import appliances.envTemp

import switches.boilerValveSwitch
import switches.channel8
import switches.simSwitch
import switches.powerSwitch
import switches.mashStirSwitch

import sensors.pyboardTempSensor
import sys
import logging
import equipment.allEquipment


def setupControllers(verbose, simulation, permissive, equipment, HWlock=True):
    controllers = ctrl.controllers.controllerList(HWlock)
    # The controllerinfo is a special snowflake that stores some extra global controller info
    # It does not do anything intelligent itherwise and will always meet target
    controllers.addController('controllerInfo', appliances.controllerinfo.controllerinfo())

    if equipment is None:
        logging.error('Equipment is None')
        return(None)
    controllers['controllerInfo'].setEquipment(equipment)

    # Timer is always required in all equipment
    controllers.addController('delayTimer', appliances.hoptimer.hoptimer())

    logging.debug("Try to find hw switches")
    if not simulation:
        logging.info("Initializing hardware")
        try:
            switch12v = switches.channel8.channel8()
        except:
            if permissive:
                logging.info("**********USB pumps not found, simulating HW")
                switch12v = switches.simSwitch.simSwitchList()
            else:
                raise Exception("USB pumps not available")
    else:
        switch12v = switches.simSwitch.simSwitchList()

    tempSensors = sensors.pyboardTempSensor.tempSensorDict()

    logging.debug("Setting up appliances")

    hwTunSwitch = switches.powerSwitch.powerSwitch(1)
    boilerSwitch = switches.powerSwitch.powerSwitch(2)
    aeratorSwitch = switch12v.getSwitch(8)
    coolerSwitch = switch12v.getSwitch(7)
    mashStirSwitch = switches.mashStirSwitch.mashStirSwitch()
    #mashStirSwitch = switches.mashStirSwitch.mashStir8800Switch()
    boilerValveSwitch = switches.boilerValveSwitch.boilerValveSwitch()
    hotWaterPumpSwitch = switch12v.getSwitch(2)
    hwCirculationSwitch = switch12v.getSwitch(1)
    wortSwitch = switch12v.getSwitch(3)
    mashCirculationSwitch = switch12v.getSwitch(4)


    if 'waterHeater' in equipment['componentlist']:
        controllers.addController('waterHeater', appliances.hotWaterTun.hwt())
        controllers['waterHeater'].connectSwitch(hwTunSwitch)
        controllers['waterHeater'].connectSensor(tempSensors.getSensor('281a7a6d0b000096'))

    if 'boiler' in equipment['componentlist']:
        controllers.addController('boiler', appliances.boiler.boiler())
        controllers['boiler'].connectSwitch(boilerSwitch)
        boilerSensor = tempSensors.getSensor('28ff916002160349')
        controllers['boiler'].connectSensor(boilerSensor)

    if 'aerator' in equipment['componentlist']:
        controllers.addController('aerator', appliances.aerator.aerator())
        controllers['aerator'].connectSwitch(aeratorSwitch)

    if 'cooler' in equipment['componentlist']:
        controllers.addController('cooler', appliances.cooler.cooler())
        # As we are using plate chller do not use cooler switch
        #controllers['cooler'].connectSwitch(switches.simSwitch.simSwitch())
        controllers['cooler'].connectSensor(boilerSensor)
        # Reuse of same switch for plate cooler as immersion cooler

    if 'plateValve' in equipment['componentlist']:
        controllers.addController('plateValve', appliances.plateValve.plateValve())
        controllers['plateValve'].connectSwitch(coolerSwitch)

    if 'mashStirrer' in equipment['componentlist']:
        controllers.addController('mashStirrer', appliances.mashStirrer.mashStirrer())
        controllers['mashStirrer'].connectSwitch(mashStirSwitch)
    if 'mashHeater' in equipment['componentlist']:
        controllers.addController('mashHeater', appliances.mashHeater.mashHeater())
        controllers['mashHeater'].connectSwitch(mashCirculationSwitch)
        controllers['mashHeater'].connectSensor(tempSensors.getSensor('28f496c156230b33'))
    elif 'mashTemp' in equipment['componentlist']:
        controllers.addController('mashTemp', appliances.mashHeater.mashHeater())
        controllers['mashTemp'].connectSwitch(mashCirculationSwitch)
        controllers['mashTemp'].connectSensor(tempSensors.getSensor('28f496c156230b33'))

    if 'boilerValve' in equipment['componentlist']:
        controllers.addController('boilerValve', appliances.boilerValve.boilerValve())
        controllers['boilerValve'].connectSwitch(boilerValveSwitch)

    if 'hotWaterPump' in equipment['componentlist']:
        controllers.addController('hotWaterPump', appliances.hwPump.hwPump())
        controllers['hotWaterPump'].connectSwitch(hotWaterPumpSwitch)

    if 'hwtVolume' in equipment['componentlist']:
        controllers.addController('hwtVolume', appliances.hwtVolume.hwtVolume())
        controllers['hwtVolume'].attachHost(controllers['hotWaterPump'])
        controllers['hwtVolume'].setMaxVol(equipment['specs']['hwtVolumeMax'])

    if 'mashVolume' in equipment['componentlist']:
        controllers.addController('mashVolume', appliances.mashVolume.mashVolume())

    if 'waterCirculationPump' in equipment['componentlist']:
        controllers.addController('waterCirculationPump',
                              appliances.circulationPump.circulationPump())
        controllers['waterCirculationPump'].connectSwitch(hwCirculationSwitch)

    if 'wortPump' in equipment['componentlist']:
        controllers.addController('wortPump', appliances.hwPump.wortPump())
        controllers['wortPump'].connectSwitch(wortSwitch)

    if 'boilerVolume' in equipment['componentlist']:
        controllers.addController('boilerVolume', appliances.boilerVolume.boilerVolume())
        controllers['boilerVolume'].attachHost(controllers['wortPump'])

    if 'dispenser' in equipment['componentlist']:
        controllers.addController('dispenser1', appliances.dispenser.dispenser(1))
        controllers.addController('dispenser2', appliances.dispenser.dispenser(2))
        controllers.addController('dispenser3', appliances.dispenser.dispenser(3))
        controllers.addController('dispenser4', appliances.dispenser.dispenser(4))


    if 'envTemp' in equipment['componentlist']:
        controllers.addController('envTemp', appliances.envTemp.envTemp())
        controllers['envTemp'].connectSensor(tempSensors.getSensor('28f496c156230b33'))

    if 'mashExitTemp' in equipment['componentlist']:
        controllers.addController('mashExitTemp', appliances.envTemp.envTemp())
        controllers['mashExitTemp'].connectSensor(tempSensors.getSensor('285a9b6c0b00007b'))


    logging.debug("appliance setup done")
    # Testing of sensor object Remove me later
    for key, c1 in controllers.items():
        c1.findOrAddSensor(controllers)
    "returning..."
    return(controllers)
