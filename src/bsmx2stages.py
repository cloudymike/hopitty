#!/usr/bin/python
"""
Reads a beersmith recipe and creates stages file
Runs basic checks against controllers

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
import ctrl
import argparse
import recipeReader
import json
import equipment
import os
import xml.etree.ElementTree
import checker
import logging

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Load files to S3')
    parser.add_argument('-i', '--inputfile', default=None, help='Input beersmith file')
    parser.add_argument('-o', '--outputfile', default=None, help='Output stages file')
    parser.add_argument('-d', '--debug', action='store_true', help='Set log level to debug')
    args = parser.parse_args()

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO


    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=loglevel,
                        stream=sys.stdout)

    if args.inputfile is None:
        inf = sys.stdin
    else:
        #testing
        print("==================================> {}".format(args.inputfile))
        
        try:
            inf = open(args.inputfile, 'r')
        except:
            print("Can not open inputfile")
            sys.exit(1)
    if args.outputfile is None:
        outf = sys.stdout
    else:
        try:
            outf = open(args.outputfile, 'w')
        except:
            print("Can not open outputfile {}".format(args.outputfile))
            sys.exit(1)
    bsmxIn = inf.read()
    bsmxStr = bsmxIn.replace('&', 'AMP')
    inf.close()
    
    e = xml.etree.ElementTree.fromstring(bsmxStr)
    equipmentName = e.find('Data').find('Recipe').find('F_R_EQUIPMENT').find('F_E_NAME').text
    print('Equipment: {}'.format(equipmentName))
    mypath = os.path.dirname(os.path.realpath(__file__))
    availableEquipment = equipment.allEquipment(mypath + '/equipment/*.yaml')
    myEquipment = availableEquipment.get(equipmentName)
    controllers = ctrl.setupControllers(False, True, True, myEquipment)

    bsmxObj = recipeReader.bsmxStages(bsmxStr, controllers)
    stagesStr = bsmxObj.getStages()
    if stagesStr is None:
        print('Error: Invalid recipe')
        sys.exit(1)

    equipmentchecker = checker.equipment(controllers, stagesStr)
    if not equipmentchecker.check():
        print("Error: equipment vs recipe validation failed")
        sys.exit(1)

    # Debug print the dispensers
    #hops = bsmxObj.ingredientsHops()
    #misc = bsmxObj.ingredientsMisc()

    json.dump(stagesStr, outf, sort_keys=True,
                           indent=2, separators=(',', ': '))
    outf.close()
    bsmxObj.compareStrikeTemp()

