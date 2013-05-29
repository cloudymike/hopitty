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
import getopt

def usage():
    print 'usage:'
    print "-h: help"
    print "-f <filepath>: File for beermith file"
    print "-u <user>: User for beermith files"
    print "-v: verbose"
    sys.exit

def getOptions():
    options, remainder = getopt.getopt(sys.argv[1:], 'f:hu:v', [
                         'file=',
                         'help',
                         'user=',
                         'verbose',
                         ])
    optret = {}
    optret['verbose'] = False
    optret['user'] = getpass.getuser()
    optret['bsmxfile'] = None

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-f', '--file'):
            optret['bsmxfile'] = arg
        if opt in ('-u', '--user'):
            optret['user'] = arg
        elif opt in ('-v', '--verbose'):
            optret['verbose'] = True
    return(optret)
 
 
if __name__ == "__main__":
    options = getOptions()
    daemon = ctrl.scanrun(options['bsmxfile'], options['user'])
    daemon.loop()
        