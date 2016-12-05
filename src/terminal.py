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
import fcntl
import os


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
        simulation = True
    print "Simulation: ", simulation
    controllers = ctrl.setupControllers(verbose, simulation, permissive)
    if HWcheck:
        if controllers.HWOK():
            logging.info('USB devices connected')
        else:
            logging.info('ERROR: Missing USB devices, exiting')
            sys.exit(1)
    loopActive = True
    
    fd = sys.stdin.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    nonblocking = fl | os.O_NONBLOCK
    blocking = fl

    while loopActive:

        # Read one of the recipe files
        if recipeFile == "":
            fcntl.fcntl(fd, fcntl.F_SETFL, blocking)
            print "Try ../jsonStages/base.golden"
            recipeFile = raw_input("Enter your filename: ")
            #recipeFile = sys.stdin.readline().rstrip()
            print "Reading file:",recipeFile
        try:
            with open(recipeFile) as data_file:    
                stages = json.load(data_file)
        except:
            stages = None
        recipeFile = ""

        if stages is None:
            print "Bad recipe file"
        else:
            equipmentchecker = checker.equipment(controllers, stages)
            if not equipmentchecker.check():
                logging.error("Error: equipment vs recipe validation failed")
                stages = None
        
            if (stages == {}) or (stages is None):
                stages = None
                
            brun = stages2beer.s2b(controllers, stages)
            brun.start()
        
            print "-------------------Running-------------------------------"
            
        
            fcntl.fcntl(fd, fcntl.F_SETFL, nonblocking)
            while not brun.stopped() and stages is not None:
                time.sleep(1)
                if brun.paused():
                    print "pause ",
                else:
                    print "run   ",
                print brun.getStage(), " ",
                sdict = brun.getStatus()
                for key, val in sdict.iteritems():
                    print val['actual'],
                print " "
                try:  input = sys.stdin.readline()
                except: continue
                print "INPUT:",input, ":"
                if input[0] == "s":
                    brun.stop()
                    print "\n-----------------Call for stop ------------------------------------"
                if input[0] == "p":
                    brun.pause()
                    print "\n-----------------Call for pause ------------------------------------"
                if input[0] == "c":
                    brun.unpause()
                    print "\n-----------------Call for continue ------------------------------------"
                if input[0] == "n":
                    brun.skip()
                    print "\n-----------------Call for next ------------------------------------"
                    
                
            print "\n-----------------Stopping------------------------------------"
            
            brun.join()

        time.sleep(1)
    
    del controllers
    sys.exit(0)
