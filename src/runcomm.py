#!/usr/bin/python

# Run simple loop but with communications



# branch t1
import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

import getopt
import ctrl
import checker.equipment
import logging
import threading
import time
import json
import equipment.allEquipment
import os
import communicate.netsock
import argparse

class deviceloop():
        
    def __init__(self,
        controllers=None,
        stages=None
       ):
        self.sc = communicate.netsock.socketcomm()
        self.oldtime = 0
        self.state='stop'
        
    
    def run(self):
        """
        Main run loop. Go through each stage of recipe and
        for each stage loop until all targets met.
        no blocking, I.e a separate thread
        """
        print("run")
        for r_key, settings in sorted(stages.items()):
            controllers.stop()
            controllers.run(settings)
            self.state='run'
            while not controllers.done() or self.state == 'pause' :
                controllers.run(settings)
                nowtime = time.time()
                deltatime = nowtime - self.oldtime
                self.oldtime = nowtime
                difftime = 1.0 - deltatime
                if abs(difftime) > 10:
                    difftime = 0
                sleeptime = max(1.0 + difftime, 0.0)
                sleeptime = min(1.0, sleeptime)
                time.sleep(sleeptime)
                controllers.logstatus()
                lightstatus = controllers.lightStatus()
                fullstatus = {}
                fullstatus['stage'] = str(r_key)
                fullstatus['state'] = str(self.state)
                fullstatus['status'] = lightstatus
                status = json.dumps(fullstatus)
                print(status)
                
                command = self.sc.read(status)
                print("Command {}".format(command))
                if 'terminate' in command:
                    self.state = 'terminate'
                    self.sc.close()
                    return()
                if 'run' in command:
                    self.state = 'run'
                if 'stop' in command:
                    self.state = 'stop'
                if 'pause' in command:
                    self.state = 'pause'
                if 'skip' in command:
                    # Skip out of while loop to step one step ahead, and start or keep running
                    self.state = 'run'
                    break


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

    parser = argparse.ArgumentParser(description='Run brew equiipment with communication enabled for control.')
    parser.add_argument('-b', '--bsmx', default=None, help='Beersmith file to use, bsmx format, ')
    parser.add_argument('-c', '--checkonly', action='store_true', help='Only check, do not brew')
    parser.add_argument('-e', '--equipment', action='store_true', help='Force use of real equipment')
    parser.add_argument('-f', '--file', default="", type=str, help='Stages file to use, json format, ')
    parser.add_argument('-q', '--quick', action='store_true', help='Run quick recipe with no delays, or meeting goals')
    parser.add_argument('-s', '--simulate', action='store_true', help='Force simulation')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='store_true', help='Print version and exit')

    args = parser.parse_args()
    permissive = True

    mypath = os.path.dirname(os.path.realpath(__file__))
    e = equipment.allEquipment.allEquipment(mypath + '/equipment/*.yaml')
    myequipment = e.get('Grain 3G, 5Gcooler, 5Gpot, platechiller')
    
    if args.equipment:
        args.simulate = False

    controllers = ctrl.setupControllers(args.verbose, args.simulate, permissive, myequipment)
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
        
    print(stages)

    equipmentchecker = checker.equipment.equipment(controllers, stages)
    
    devices = deviceloop(controllers, stages)
    
    if not equipmentchecker.check():
        logging.error("Error: equipment vs recipe validation failed")

    if not args.checkonly:
        if (stages != {}) and (stages is not None):
            devices.run()


    logging.info(" ")
    logging.info("OK")
    logging.info("Shutting down")
    del controllers

    sys.exit(0)
