#!/usr/bin/python
"""
Reads a beersmith recipe and creates stages file
Runs basic checks against controllers

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
import ctrl
import getopt
import recipeReader
import json
import equipment
import os
import xml.etree.ElementTree
import checker

def usage():
    print 'usage:'
    print "-h: help"
    print "-i <filepath>: Input beersmith file"
    print "-o <filepath>: output stages file"
    print "-v: verbose"
    sys.exit(0)


def getOptions():
    options, remainder = getopt.getopt(sys.argv[1:], 'i:ho:v', [
        'input=',
        'help',
        'output=',
        'verbose',
        ])
    optret = {}
    optret['verbose'] = False
    optret['inputfile'] = None
    optret['outputfile'] = None

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-i', '--inputfile'):
            optret['inputfile'] = arg
        if opt in ('-o', '--outputfile'):
            optret['outputfile'] = arg
        elif opt in ('-v', '--verbose'):
            optret['verbose'] = True
    return(optret)

if __name__ == "__main__":
    options = getOptions()

    if options['inputfile'] is None:
        inf = sys.stdin
    else:
        #testing
        print "==================================>", options['inputfile']
        
        try:
            inf = open(options['inputfile'], 'r')
        except:
            print "Can not open inputfile"
            sys.exit(1)
    if options['outputfile'] is None:
        outf = sys.stdout
    else:
        try:
            outf = open(options['outputfile'], 'w')
        except:
            print "Can not open outputfile", options['outputfile']
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

    bsmxObj = recipeReader.bsmxStages(bsmxStr, controllers, myEquipment)
    stagesStr = bsmxObj.getStages()
    if stagesStr is None:
        print('Error: Invalid recipe')
        sys.exit(1)

    equipmentchecker = checker.equipment(controllers, stagesStr)
    if not equipmentchecker.check():
        print("Error: equipment vs recipe validation failed")
        sys.exit(1)

    hops = bsmxObj.ingredientsHops()
    json.dump(stagesStr, outf, sort_keys=True,
                           indent=2, separators=(',', ': '))
    outf.close()
    bsmxObj.compareStrikeTemp()

