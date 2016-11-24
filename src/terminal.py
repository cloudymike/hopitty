#!/usr/bin/python

# branch t1
import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

import getopt
import ctrl
import recipeReader
import stages2beer
import checker
import logging
import threading
import time
import json


def usage():
    print 'usage:'
    print "-h: help"
    print "-c: checkonly"
    print "-f file: read JSON file"
    print "-q: quick check"
    print "-e: Equipment check"
    print "-v: verbose"
    sys.exit

def end_now(logging):
    logging.info(" ")
    logging.info("OK")
    logging.info("Shutting down")
    sys.exit(0)
    
if __name__ == "__main__":
#    simTemp = 70
#    shutdown = False

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.warning('warning test')
    logging.info('Starting...')

    options, remainder = getopt.getopt(sys.argv[1:], 'cef:hqpuv', [
        'checkonly',
        'equipment',
        'file=',
        'help',
        'printRecipe',
        'quick',
        'verbose',
        'version=',
        ])
    verbose = False
    simulation = False
    permissive = True
    quick = False
    checkonly = False
    printRecipe = False
    HWcheck = False
    recipeFile = ""
    bsmxFile = ""
    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-f', '--file'):
            recipeFile = arg
        elif opt in ('-q', '--quick'):
            quick = True
        elif opt in ('-c', '--checkonly'):
            checkonly = True
        elif opt in ('-p', '--printRecipe'):
            printRecipe = True
        elif opt in ('-e', '--equipment'):
            HWcheck = True
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt == '--version':
            version = arg

    # If hardware requirement is set, 
    # check that hardware is connected
    if HWcheck:
        simulation = (simulation or (not HWcheck))
    else:
        simulation = False
    controllers = ctrl.setupControllers(verbose, simulation, permissive)
    if HWcheck:
        if controllers.HWOK():
            logging.info('USB devices connected')
        else:
            logging.info('ERROR: Missing USB devices, exiting')
            sys.exit(1)

    # Read one of the recipe files
    if recipeFile != "":
        with open(recipeFile) as data_file:    
            stages = json.load(data_file)
    else:
        stages = {}

    equipmentchecker = checker.equipment(controllers, stages)
    if not equipmentchecker.check():
        logging.error("Error: equipment vs recipe validation failed")

    if checkonly:
        end_now(logging)
    if (stages == {}) or (stages is None):
        end_now(logging)
        
    brun = stages2beer.s2b(controllers, stages)
    brun.start()

    print "-------------------Running-------------------------------"
    
    while not brun.stopped():
        try: input = sys.stdin.readline()
        except: continue
        print "INPUT:",input, ":"
        if input[0] == "s":
            brun.stop()
            print "-----------------Call for stop ------------------------------------"
            
        
    print "-----------------Stopping------------------------------------"
    
    brun.join()
    
    del controllers
    sys.exit(0)
