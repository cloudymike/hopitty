#!/usr/bin/python
"""
Scans the recipe database and creates recipeListClass object
Also pushes recipe name list to memcache for use by web pages

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/recipelistmgr")
import getpass
import os
import recipelistmgr
import time
import ctrl
import dataMemcache
import stages2beer
import getopt
from os import path, access, R_OK  # W_OK for write permission.
import checker
import recipeReader


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
    rl = recipelistmgr.recipeListClass()
    mydata = dataMemcache.brewData()

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
    rl.readBeerSmith(bsmxfile)
    iterlist = rl.getlist()
    deleteList = []
    for recipeName in iterlist:
        recipeObjBsmx = rl.getRecipe(recipeName)
        recipeBSMX = recipeObjBsmx.getBSMXdoc()
        recipeObjParsed = recipeReader.bsmxStages(recipeBSMX, controllers)
        if not recipeObjParsed.isValid():
            deleteList.append(recipeName)
            print "**********Fail on parseBSMX:", recipeName
        else:
            ce = checker.equipment(controllers, recipeObjParsed.getStages())
            if not ce.check():
                deleteList.append(recipeName)
                print "**********Fail on equipment check:", recipeName
    for deleteName in deleteList:
        rl.deleteRecipe(deleteName)

    rl.nameListToMemcache()
    return(rl)


if __name__ == "__main__":
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
    brewdaemon = stages2beer.brewloop(controllers, recipelist, 1)
    brewdaemon.start()
    print "Started brew daemon"
    brewdaemon.join()
    print 'Done!'
