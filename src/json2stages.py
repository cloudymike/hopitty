#!/usr/bin/python
"""
Scans the recipe database and creates recipeListClass object
Also pushes recipe name list to memcache for use by web pages

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
import ctrl
import argparse
import recipeReader
import json
import equipment
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate recipe to json')
    parser.add_argument('-i', '--inputfile', default=None, help='Input json file')
    parser.add_argument('-o', '--outputfile', default=None, help='Output stages file')
    parser.add_argument('-e', '--equipment', default=None, help='Equipment to use')
    args = parser.parse_args()

    mypath = os.path.dirname(os.path.realpath(__file__))
    e = equipment.allEquipment(mypath + '/equipment/*.yaml')
    if args.equipment is None:
        myequipment = e.get('Grain 3G, 5Gcooler, 5Gpot, platechiller')
    else:
        myequipment = e.get(args.equipment)
    print(myequipment)
    controllers = ctrl.setupControllers(False, True, True, myequipment)
    if args.inputfile is None:
        inf = sys.stdin
    else:
        try:
            inf = open(args.inputfile, 'r')
        except:
            print("Can not open inputfile {}".format(args.inputfile))
            sys.exit(1)
    if args.outputfile is None:
        outf = sys.stdout
    else:
        try:
            outf = open(args.outputfile, 'w')
        except:
            print("Can not open outputfile {}".format(args.outputfile))
            sys.exit(1)
    jsonStr = inf.read()
    inf.close()
    jsonObj = recipeReader.jsonStages(jsonStr, controllers)
    stagesStr = jsonObj.getStages()
    json.dump(stagesStr, outf, sort_keys=True,
                           indent=2, separators=(',', ': '))
    outf.close()
