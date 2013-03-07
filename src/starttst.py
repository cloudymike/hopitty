#!/usr/bin/python

# branch t1
import sys

import pickle
import time
import getopt
import sys
import appliances
import ctrl
#import ctrl.controllers
import ctrl.readRecipe
#import ctrl.checkers
import appliances.boiler
#import ctrl.checkers
import switches
import memcache
#@PydevCodeAnalysisIgnore


if __name__ == "__main__":
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    while True:
        try:
            runStatus = mc.get('runStatus')
        except:
            runStatus = ""
        if runStatus == "run":
            print "Running...",
            sys.stdout.flush()
            time.sleep(5)
            mc.set("runStatus", 'stop')
            print "Stopped"
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)
        

    sys.exit()
