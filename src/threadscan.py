#!/usr/bin/python
"""
Scans the recipe database and creates recipeListClass object
Also pushes recipe name list to memcache for use by web pages

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
import getpass
import ctrl
import argparse
from os import path, access, R_OK  # W_OK for write permission.
import checker
import recipeReader
import webctrl
import recipeModel
import logging
import equipment


def readRecipeFile(ctrl, recipefile=None, user=None, download=False):
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

    if bsmxfile is not None and path.isfile(bsmxfile) and access(bsmxfile, R_OK):
        print "BSMX File", bsmxfile, "exists and is readable"
    else:
        if not download:
            print "ERROR: BSMX file", bsmxfile,\
                  "is missing or is not readable"
        bsmxfile = None

    rlUpdate = updateRecipes(rl, bsmxfile, download)
    print "================ Recipe List ==============="
    rlUpdate.printNameList()
    print "============================================"
    return(rlUpdate)


def updateRecipes(rl, bsmxfile, download):
    """
    Update Recipe list by removing all recipes that does not work.
    This is checked by doing a check against recipe and equipment
    """
    if download:
        rl.downloadBeerSmith()
    else:
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
    return(rl)


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.warning('warning test')
    logging.info('Starting...')

    parser = argparse.ArgumentParser(description='Run a json or bsmx file')
    filegroup = parser.add_mutually_exclusive_group(required=True)
    filegroup.add_argument('-f', '--file', default=None, help='Input BSMX file')
    filegroup.add_argument('-u', '--user', default=None, help='User for home dir to check')
    filegroup.add_argument('-d', '--download', action='store_true', help='Download BSMX file')
    parser.add_argument('-t', '--equipmentType', default='', help='Type of equipment to use')
    parser.add_argument('-e', '--equipment', action='store_true', help='Equipment check')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()
    
    e = equipment.allEquipment('equipment/*.yaml')
    if args.equipmentType:
        myequipment = e.get(args.equipmentType)
    else:
        myequipment = e.get('Grain 3G, 5Gcooler, 5Gpot, platechiller')
        
    controllers = ctrl.setupControllers(args.verbose, False, True, myequipment)
    if args.equipment:
        if controllers.HWOK():
            print "HW OK"
        else:
            print "ERROR: HW not OK, exiting"
            sys.exit(1)

    recipelist = readRecipeFile(controllers,
                                args.file,
                                args.user,
                                args.download)
    if recipelist is None:
        print "Error: No recipes"
        sys.exit(1)

    # Start daemon loop
    print "Starting brew daemon"
    brewdaemon = webctrl.runbrew(controllers, recipelist)
    brewdaemon.startBlocking()
    print 'Done!'
