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


def usage():
    print 'usage:'
    print "-h: help"
    print "-b file: read beersmith file"
    print "-c: checkonly"
    print "-f file: read JSON file"
    print "-q: quick check"
    print "-e: Equipment check"
    print "-v: verbose"
    sys.exit


if __name__ == "__main__":
#    simTemp = 70
#    shutdown = False

    options, remainder = getopt.getopt(sys.argv[1:], 'b:cef:hqpuv', [
        'bsmx=',
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
        if opt in ('-b', '--bsmx'):
            bsmxFile = arg
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

    stages = {}
    recipeName = ""
    simulation = (simulation or (not HWcheck))
    controllers = ctrl.setupControllers(verbose, simulation, permissive)

    if HWcheck:
        if controllers.HWOK():
            print('USB devices connected')
        else:
            print('ERROR: Missing USB devices, exiting')
            sys.exit(1)

    # Read one of the recipe files
    if recipeFile != "":
        j = recipeReader.jsonStages(recipeFile, controllers)
        if not j.isValid():
            print "Error: bad recipe"
        else:
            recipeName = j.getRecipeName()
            stages = j.getStages()
    elif bsmxFile != "":
        b = recipeReader.bsmxStages(bsmxFile, controllers)
        if not b.isValid():
            print "Error: bad recipe"
        else:
            recipeName = b.getRecipeName()
            stages = b.getStages()
    else:
        recipeName = ""
        stages = {}

    equipmentchecker = checker.equipment(controllers, stages)
    if not equipmentchecker.check():
        print"Error: equipment vs recipe validation failed"

    print "Running ", recipeName

    if (stages != {}) and (stages is not None):
        brun = stages2beer.s2b(controllers, stages)
        if checkonly:
            if brun.check():
                print "Check OK"
            else:
                print "ERROR: Check failed"
                sys.exit(1)
        elif quick:
            if brun.quickRun():
                print "Quick run OK"
            else:
                print "ERROR: Quick run failed"
                sys.exit(1)
        else:
            brun.start()
            brun.join()

        if not brun.OK():
            print "ERROR: Run of controller failed"
            del brun
            sys.exit(1)
        del brun

    print " "
    print "OK"
    print "Shutting down"
    del controllers

    sys.exit(0)
