
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
    # Try to find hw switches
    if not simulation:
        logging.info("Initializing hardware")

    logging.info("Setting up appliances")

    hwTunSwitch = switches.simSwitch()

    controllers.addController('waterHeater', appliances.hwt())
    controllers['waterHeater'].connectSwitch(hwTunSwitch)
    controllers.addController('delayTimer', appliances.hoptimer())

    logging.info("appliance setup done")
    # Testing of sensor object Remove me later
    for key, c1 in controllers.items():
        c1.findOrAddSensor(controllers)
        # print key
    "returning..."
    return(controllers)
