#!/usr/bin/python
"""
Scans the recipe database and creates recipeListClass object
Also pushes recipe name list to memcache for use by web pages

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
import getpass
import ctrl
import getopt
from os import path, access, R_OK  # W_OK for write permission.
import checker
import recipeReader
import webctrl
import recipeModel
import logging


def usage():
    print 'usage:'
    print "-h: help"
    print "-f <filepath>: File for beermith file"
    print "-u <user>: User for beermith files"
    print "-v: verbose"
    sys.exit(0)


def getOptions():
    options, remainder = getopt.getopt(sys.argv[1:], 'ef:hu:v', [
        'equipment',
        'file=',
        'help',
        'user=',
        'verbose',
        ])
    optret = {}
    optret['verbose'] = False
    optret['user'] = getpass.getuser()
    optret['bsmxfile'] = None
    optret['HWcheck'] = False

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-e', '--equipment'):
            optret['HWcheck'] = True
        if opt in ('-f', '--file'):
            optret['bsmxfile'] = arg
        if opt in ('-u', '--user'):
            optret['user'] = arg
        elif opt in ('-v', '--verbose'):
            optret['verbose'] = True
    return(optret)


def readRecipeFile(ctrl, recipefile=None, user=None):
    rl = recipeModel.RecipeList()

    # Try to find a recipe file
    if recipefile is not None:
        bsmxfile = recipefile
    elif user is not None:
        bsmxfile = "/home/" + user + "/.beersmith2/Cloud.bsmx"
    else:
        print "ERROR: No data for BSMX file"
        bsmxfile = None

    print bsmxfile

    if path.isfile(bsmxfile) and access(bsmxfile, R_OK):
        print "BSMX File", bsmxfile, "exists and is readable"
    else:
        print "ERROR: BSMX file", bsmxfile,\
              "is missing or is not readable"
        bsmxfile = None

    rlUpdate = updateRecipes(rl, bsmxfile)
    print "================ Recipe List ==============="
    rlUpdate.printNameList()
    print "============================================"
    return(rlUpdate)


def updateRecipes(rl, bsmxfile):
    """
    Update Recipe list by removing all recipes that does not work.
    This is checked by doing a check against recipe and equipment
    """
    rl.readBeerSmith(bsmxfile)
    iterlist = rl.getlist()
    deleteList = []
    for recipeName in iterlist:
        recipeObjBsmx = rl.getRecipe(recipeName)
        recipeBSMX = recipeObjBsmx.getBSMXstring()
        recipeObjParsed = recipeReader.bsmxStages(recipeBSMX, controllers)
        if not recipeObjParsed.isValid():
            deleteList.append(recipeName)
            logging.info("**********Fail on parseBSMX:" + recipeName)
        else:
            ce = checker.equipment(controllers, recipeObjParsed.getStages())
            if not ce.check():
                deleteList.append(recipeName)
                logging.info("**********Fail on equipment check:" + recipeName)
    for deleteName in deleteList:
        logging.info("deleting" + deleteName)
        rl.deleteRecipe(deleteName)

    #rl.nameListToMemcache()
    return(rl)


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.warning('warning test')
    logging.info('Starting...')

    options = getOptions()
    controllers = ctrl.setupControllers(options['verbose'], False, True)
    if options['HWcheck']:
        if controllers.HWOK():
            print "HW OK"
        else:
            print "ERROR: HW not OK, exiting"
            sys.exit(1)

    recipelist = readRecipeFile(controllers,
                                options['bsmxfile'],
                                options['user'])
    if recipelist is None:
        print "Error: No recipes"
        sys.exit(1)

    # Start daemon loop
    print "Starting brew daemon"
    brewdaemon = webctrl.runbrew(controllers, recipelist)
    brewdaemon.startBlocking()
    print 'Done!'
