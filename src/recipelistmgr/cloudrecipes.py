#!/usr/bin/python
"""
Handles recipe collection as objects
Reading from bsmx also included
To be used by other modules, including web server
"""

# TODO
# Use defs from controller...

import sys
import pickle
import xml.dom.minidom
#import xml.etree.ElementTree as ET
import types
import memcache
#@PydevCodeAnalysisIgnore
import recipelistmgr
import time


def objectFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    pickledObject = mc.get(key)
    object = pickle.loads(pickledObject)
    return(object)


def getListFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    recipeNameList = mc.get(key)
    return(recipeNameList)


if __name__ == "__main__":

    print "Alive"
    rl = recipelistmgr.recipeListClass()
    for n in range(1, 10):
        rl.readBeerSmith('/home/mikael/.beersmith2/Cloud.bsmx')
        rl.storeToMemcache()
        #rlPickle = rl.pickleMe()
        rl.nameListToMemcache()
        print rl.len()
        time.sleep(10)
        rnl = getListFromMemcache('recipeNameList')
        for rn in rnl:
            print rn
