#!/usr/bin/python
"""
Scans the recipe database and creates recipeListClass object
Also pushes recipe name list to memcache for use by web pages

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/recipelistmgr")
import ctrl
import getopt
import recipeReader
import json


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
    controllers = ctrl.setupControllers(False, True, True)
    if options['inputfile'] is None:
        inf = sys.stdin
    else:
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
    bsmxStr = inf.read()
    inf.close()
    bsmxObj = recipeReader.bsmxStages(bsmxStr, controllers)
    stagesStr = bsmxObj.getStages()
    stagesJson = json.dump(stagesStr, outf, sort_keys=True,
                           indent=2, separators=(',', ': '))
    outf.close()