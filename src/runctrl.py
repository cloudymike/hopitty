#!/usr/bin/python

# branch t1
import sys
sys.path.append("/home/mikael/workspace/hoppity/src") 
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

#import pickle
#import time
import getopt
#import sys
#import appliances
import ctrl
#import ctrl.controllers
#import ctrl.readRecipe
#import ctrl.checkers
#import appliances.boiler
#import ctrl.checkers
#import switches
#import memcache
#@PydevCodeAnalysisIgnore

def usage():
    print 'usage:'
    print "-h: help"
    print "-b file: read beersmith file"
    print "-f file: read JSON file"
    print "-q: quick check"
    print "-v: verbose"
    sys.exit



if __name__ == "__main__":
#    simTemp = 70
#    shutdown = False

    options, remainder = getopt.getopt(sys.argv[1:], 'b:f:hqv', [
                         'bsmx=',
                         'file=',
                         'help',
                         'quick',
                         'verbose',
                         'version=',
                         ])
    verbose = False
    simulation = False
    permissive = True
    quick = False
    recipeFile = ""
    bsmxFile = ""
    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-f', '--file'):
            recipeFile = arg
        if opt in ('-b', '--bsmx'):
            bsmxFile = arg
        elif opt in ('-q', '--quick'):
            quick = True
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt == '--version':
            version = arg

    ru = ctrl.rununit()
    if bsmxFile != "":
        xml = ctrl.bsmxReadFile(bsmxFile)
        ru.bsmxIn(xml)
    else:
        json = ctrl.readJson(recipeFile)
        ru.jsonIn(json)

    if quick:
        runOK = ru.quick()
    else:
        runOK = ru.run()

    if not runOK:
        print "ERROR: Run of controller failed"
        sys.exit(1)

    print " "
    print "OK"
    ru.stop()
    print "Shutting down"
    del ru

    sys.exit()
