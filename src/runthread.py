#!/usr/bin/python

# branch t1
import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

import argparse
import ctrl
import recipeReader
import stages2beer.s2b
import checker.equipment
import logging
import threading
import time
import equipment.allEquipment
import os
import xml.etree.ElementTree
import requests
import xmltodict


if __name__ == "__main__":
#    simTemp = 70
#    shutdown = False
    permissive = True

    parser = argparse.ArgumentParser(description='Run a json or bsmx file')
    filegroup = parser.add_mutually_exclusive_group(required=True)
    filegroup.add_argument('-f', '--file', default="", help='Input JSON file')
    filegroup.add_argument('-b', '--bsmx', default="", help='Input BeerSmith file')
    filegroup.add_argument('-d', '--download', default="", help='BeerSmith file to download')

    parser.add_argument('-q', '--quick', action='store_true', help='Quick check')
    parser.add_argument('-c', '--checkonly', action='store_true', help='Check only')
    #parser.add_argument('-p', '--printRecipe', action='store_true', help='Print recipe')
    parser.add_argument('-e', '--equipment', action='store_true', help='Equipment check')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        logginglevel = logging.DEBUG
    else:
        logginglevel = logging.ERROR

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logginglevel,
                        stream=sys.stdout)

    logging.info('Starting...')


    stages = {}
    recipeName = ""
    if args.equipment:
        simulation = (simulation or (not args.equipment))
    else:
        simulation = False
        
    mypath = os.path.dirname(os.path.realpath(__file__))
    availableEquipment = equipment.allEquipment.allEquipment(mypath + '/equipment/*.yaml')

    bsmxIn = None
    if args.bsmx != "":
        try:
            inf = open(args.bsmx, 'r')
        except:
            logging.error('Can not read file: {}'.format(args.bsmx))
            sys.exit(1)
        bsmxIn = inf.read()
        inf.close()
        bsmxStr = bsmxIn.replace('&', 'AMP')
        print(bsmxStr)
        try:
            e = xml.etree.ElementTree.fromstring(bsmxStr)
        except:
            logging.error('Can not parse file: {}'.format(args.bsmx))
        equipmentName = e.find('Data').find('Recipe').find('F_R_EQUIPMENT').find('F_E_NAME').text
        myEquipment = availableEquipment.get(equipmentName)
        if myEquipment is None:
            logging.error('Selected equipment is not available')
            sys.exit(1)

    if args.download != "":
        try:
            urlified = str(args.download)
            urlified.encode('utf-8')
            urlified = urlified.replace(' ','_')
            print(urlified)
            print(urlified[4])
            downloadurl = 'http://beersmithrecipes.s3-website.us-west-2.amazonaws.com/{}.bsmx'.format(urlified)
            print(downloadurl)
            i = requests.get(downloadurl)
            bsmxIn = str(i.content)
        except:
            logging.error('Can not download: {}'.format(args.download))
            sys.exit(1)
        bsmxIn = bsmxIn.encode('utf-8')
        bsmxStr = bsmxIn.replace('&', 'AMP')
        xmldict = xmltodict.parse(bsmxStr)
        equipmentName = xmldict['Cloud']['F_R_EQUIP_NAME']
        myEquipment = availableEquipment.get(equipmentName)
        if myEquipment is None:
            logging.error('Selected equipment is not available')
            sys.exit(1)

    if bsmxIn is None:
        # This may have to change to AllNoLimit
        myEquipment = availableEquipment.get('Grain 3G, 5Gcooler, 5Gpot, platechiller')

    logging.info('Equipment: {}'.format(myEquipment['equipmentName']))
    
    controllers = ctrl.setupControllers(args.verbose, simulation, permissive, myEquipment)
    if controllers is None:
        logging.error('No controllers')
        sys.exit(1)

    if args.equipment:
        if controllers.HWOK():
            logging.info('USB devices connected')
        else:
            logging.info('ERROR: Missing USB devices, exiting')
            sys.exit(1)

    # Read one of the recipe files
    if args.file != "":
        j = recipeReader.jsonStages(args.file, controllers)
        if not j.isValid():
            logging.error("Error: bad json recipe")
        else:
            recipeName = j.getRecipeName()
            stages = j.getStages()
    elif args.bsmx != "" :
        b = recipeReader.bsmxStages(args.bsmx, controllers)
        if not b.isValid():
            logging.error("Error: bad bsmx recipe")
            sys.exit(1)
        else:
            recipeName = b.getRecipeName()
            stages = b.getStages()
    elif args.download != "":
        b = recipeReader.bsmxStages(bsmxStr, controllers)
        if not b.isValid():
            logging.error("Error: bad bsmx recipe")
            sys.exit(1)
        else:
            recipeName = b.getRecipeName()
            stages = b.getStages()
    else:
        recipeName = ""
        stages = {}

    equipmentchecker = checker.equipment.equipment(controllers, stages)
    if not equipmentchecker.check():
        logging.error("Error: equipment vs recipe validation failed")
        sys.exit(1)

    logging.info("Running " + recipeName)

    if (stages != {}) and (stages is not None):
        brun = stages2beer.s2b.s2b(controllers, stages)
        dl = ctrl.datalogger(controllers)

        if args.checkonly:
            if brun.check():
                logging.info("Check OK")
            else:
                logging.info("ERROR: Check failed")
                sys.exit(1)
        elif args.quick:
            if brun.quickRun():
                logging.info("Quick run OK")
            else:
                logging.error("ERROR: Quick run failed")
                sys.exit(1)
        else:
            brun.start()
            dl.start()
            brun.join()
            dl.stop()

        if not brun.OK():
            logging.error("ERROR: Run of controller failed")
            del brun
            sys.exit(1)
        del brun
        del dl

    logging.info(" ")
    logging.info("OK")
    logging.info("Shutting down")
    del controllers

    sys.exit(0)
