#!/usr/bin/python
"""
Scans the recipe database and creates recipeListClass object
Also pushes recipe name list to memcache for use by web pages

"""

# TODO
# Use defs from controller...

import sys
sys.path.append("/home/mikael/workspace/hoppity/src") 
sys.path.append("/home/mikael/workspace/hoppity/src/recipelistmgr")

import pickle
import xml.dom.minidom
#import xml.etree.ElementTree as ET
import types
import memcache
#@PydevCodeAnalysisIgnore
import recipelistmgr
import time

user = 'mikael'

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
        bsmxfile = "/home/"+user+"/.beersmith2/Cloud.bsmx"
        rl.readBeerSmith(bsmxfile)
        rl.storeToMemcache()
        #rlPickle = rl.pickleMe()
        rl.nameListToMemcache()
        print rl.len()
        time.sleep(10)
