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
import ctrl
import recipelistmgr

#===========================================================

def objectFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    pickledObject = mc.get(key)
    object = pickle.loads(pickledObject)
    return(object)


#======================== Nose test defs =============================
def recipeEquivalence(recipe1, recipe2):
    assert recipe1.getName() == recipe2.getName()


def listEquivalence(list1, list2):
    assert len(list1.list) == len(list2.list)


def getTestRecipeList():
    """ Get recipe list in test directory, and return a recipe list"""
    rl = recipelist.recipeListClass()
    rl.readBeerSmith('../tests/Cloud.bsmx')
    return(rl)


def testReading():
    """ Do a check that recipe list read in is a valid set of recipes
        Be thorough, as all other check are compared against the original
        list.
    """

    rl = getTestRecipeList()
    assert len(rl.list) > 0
    for name, recipe in rl.list.items():
        assert len(name) > 0
        assert isinstance(name, types.StringTypes)
        assert name == recipe.getName()

        # Checks on each recipe
        assert isinstance(recipe.getEquipment(), types.StringTypes)
        assert len(recipe.getEquipment()) > 0
        recipe.checkPopulation()

    #rl.printNameList()
    print "testReading passed"


def testPickle():
    rOrg = getTestRecipeList()
    rPickle = rOrg.pickleMe()
    rNew = pickle.loads(rPickle)
    listEquivalence(rOrg, rNew)
    #rNew.printNameList()
    print "testPickle passed"


def testMemcache():
    rOrg = getTestRecipeList()
    rOrg.storeToMemcache()
    rNew = objectFromMemcache("recipeList")
    #rNew = recipeListClass("recipeList")
    listEquivalence(rOrg, rNew)
    #rNew.printNameList()
    print "testMemcache passed"


def testEqualCheck():
    """this is testing the test tools, so should pass"""
    l1 = getTestRecipeList()
    l2 = getTestRecipeList()
    listEquivalence(l1, l2)
    print "testEqualCheck passed"

if __name__ == "__main__":
    """
    This is an example file, reading some useful value in a recipe file
    Mostly for debugging
    """
    testReading()
    testEqualCheck()
    testPickle()
    testMemcache()
