#!/usr/bin/python

# branch t1
import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

import getopt
import ctrl
import dataMemcache
import recipeReader


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

    ru = ctrl.rununit()
    if HWcheck:
        if ru.HWOK():
            print('USB devices connected')
        else:
            print('ERROR: Missing USB devices, exiting')
            sys.exit(1)

    if bsmxFile != "":
        #xml = ctrl.bsmxReadFile(bsmxFile)
        ru.bsmxIn(bsmxFile)
    else:
        #json = ctrl.readJson(recipeFile)
        #ru.jsonIn(json)
        js = recipeReader.jsonStages(recipeFile, ru.getControllers())
        if js.isValid():
            ru.stagesIn(js.getStages())
        else:
            print "ERROR: JSON file is not valid"
            sys.exit(1)

    myData = dataMemcache.brewData()
    myData.setCtrlRunning(True)

    if bsmxFile != "":
        runOK = ru.checkBSMX(bsmxFile)
    else:
        runOK = ru.check()
    if not checkonly:
        if quick:
            runOK = ru.quick()
        else:
            print "Run full"
            runOK = ru.run()

    if not runOK:
        print "ERROR: Run of controller failed"
        sys.exit(1)

    print " "
    print "OK"
    ru.stop()

    ru.prettyPrintStages()
    print "Shutting down"
    del ru

    sys.exit()
