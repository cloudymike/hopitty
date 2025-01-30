#!/usr/bin/python

# branch t1
import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

import argparse
import ctrl
import recipeReader
import checker.equipment
import logging
import threading
import time
import json
import equipment.allEquipment
import os



def run(stages, controllers):
    """
    Main run loop. Go through each stage of recipe and
    for each stage loop until all targets met.
    no blocking, I.e a separate thread
    """
    #self.runOK = self.check()
    print "run"
    #if not self.runOK:
    #    print "check failed"
    #    return
    oldtime = 0
    for r_key, settings in sorted(stages.items()):
        controllers.stop()
        controllers.run(settings)
        while not controllers.done() :
            controllers.run(settings)
            nowtime = time.time()
            deltatime = nowtime - oldtime
            oldtime = nowtime
            difftime = 1.0 - deltatime
            if abs(difftime) > 10:
                difftime = 0
            sleeptime = max(1.0 + difftime, 0.0)
            sleeptime = min(1.0, sleeptime)
            time.sleep(sleeptime)
            controllers.logstatus()
    #self.controllers.stop()


if __name__ == "__main__":
#    simTemp = 70
#    shutdown = False

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.warning('warning test')
    logging.info('Starting...')



    permissive = True

    parser = argparse.ArgumentParser(description='Run raw json file')
    parser.add_argument('-f', '--file', default="", help='Input JSON file')
    parser.add_argument('-c', '--checkonly', action='store_true', help='Check only')
    parser.add_argument('-e', '--equipment', action='store_true', help='Equipment check')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # If hardware requirement is set,
    # check that hardware is connected
    if args.equipment:
        simulation = (simulation or (not args.equipment))
    else:
        simulation = False

    mypath = os.path.dirname(os.path.realpath(__file__))
    e = equipment.allEquipment.allEquipment(mypath + '/equipment/*.yaml')
    myequipment = e.get('Grain 3G, 5Gcooler, 5Gpot, platechiller')

    controllers = ctrl.setupControllers(args.verbose, simulation, permissive, myequipment, False)
    if args.equipment:
        if controllers.HWOK():
            logging.info('USB devices connected')
        else:
            logging.info('ERROR: Missing USB devices, exiting')
            sys.exit(1)

    # Read one of the recipe files
    if args.file != "":
        with open(args.file) as data_file:
            stages = json.load(data_file)
    else:
        stages = {}

    equipmentchecker = checker.equipment.equipment(controllers, stages)
    if not equipmentchecker.check():
        logging.error("Error: equipment vs recipe validation failed")

    if not args.checkonly:
        if (stages != {}) and (stages is not None):
            run(stages, controllers)


    logging.info(" ")
    logging.info("OK")
    logging.info("Shutting down")
    del controllers

    sys.exit(0)
