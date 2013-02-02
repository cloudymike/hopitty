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


def bsmxReadString(doc, tagName):
    recipeStringNode = doc.getElementsByTagName(tagName)
    recipeString = recipeStringNode[0].firstChild.nodeValue
    return(recipeString)


def bsmxReadTempF(doc, tagName):
    return(float(bsmxReadString(doc, tagName)))


def bsmxReadTimeMin(doc, tagName):
    return(float(bsmxReadString(doc, tagName)))


def bsmxReadVolQt(doc, tagName):
    return(float(bsmxReadString(doc, tagName)) / 32)


def bsmxReadVolG(doc, tagName):
    return(float(bsmxReadString(doc, tagName)) / 128)


def bsmxReadWeightLb(doc, tagName):
    return(float(bsmxReadString(doc, tagName)) / 16)


class recipeClass():
    def __init__(self, name):
        # All pertinent data in the recipe listed below
        self.name = name
        self.equipment = None
        self.mashMethod = None
        self.infusionTemp = None
        self.mashTime = None
        self.infuseVolNet = None
        self.infuseVolTot = None
        self.tunDeadSpace = None
        self.grainAbsorption = None
        self.preboilVol = None
        self.spargeTemp = None
        self.grainWeight = None

        # Alternative Data store
        self.recipeDict = {}
        self.recipeDict['equipment'] = None

    def checkPopulation(self):
        for key, val in self.recipeDict.items():
            assert val != None

    def getValue(self, key, value):
        if key in self.recipeDict:
            self.recipeDict[key] = value
        else:
            print "Error: recipe key "
            sys.exit(1)

    def readBMXdoc(self, doc):
        self.setEquipment(bsmxReadString(doc, "F_E_NAME"))
        self.recipeDict['equipment'] = bsmxReadString(doc, "F_E_NAME")

    def printRecipeInfo(self):
        print "    ", self.getEquipment()
        print "    ", self.recipeDict['equipment']

    def setEquipment(self, equipment):
        self.equipment = equipment

    def getEquipment(self):
        return(self.equipment)

    def getName(self):
        return self.name


#===========================================================
class recipeListClass():
    def __init__(self, key=None):
        self.list = {}

    def newRecipe(self, name):
        self.list[name] = recipeClass(name)
        return(self.list[name])

    def storeToMemcache(self):
        """ Stores the class data into memcache record """
        rPickle = self.pickleMe()
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        mc.set("recipeList", rPickle)

    def loadFromMemcache(self):
        """ Loads all data from memcache record """
        pass

    def printNameList(self):
        """ Writes a list of all the recipe names"""
        for key, recipe in self.list.items():
            print key

    def printAll(self):
        """ Writes a list of all the recipe names"""
        for key, recipe in self.list.items():
            print key
            recipe.printRecipeInfo()

    def readBMXdoc(self, doc):
        cloudRecipes = doc.getElementsByTagName("Cloud")
        for recipe in cloudRecipes:
            name = bsmxReadString(recipe, "F_R_NAME")
            r = self.newRecipe(name)
            r.readBMXdoc(recipe)
            #r.setEquipment(bsmxReadString(recipe, "F_E_NAME"))

    def readBeerSmithFile(self, fileName):
        bsmxFD = open(fileName)
        bsmxRawData = bsmxFD.read()
        bsmxFD.close()

        bsmxCleanData = bsmxRawData.replace('&', 'AMP')
        doc = xml.dom.minidom.parseString(bsmxCleanData)
        return(doc)

    def readBeerSmith(self, fileName):
        doc = self.readBeerSmithFile(fileName)
        self.readBMXdoc(doc)

    def pickleMe(self):
        rPickle = pickle.dumps(self)
        return(rPickle)

    def unPickleMe(self, rPickle):
        rPickle = pickle.dumps(self)
        return(rPickle)


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
    rl = recipeListClass()
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

    print "Alive"
    rl = recipeListClass()
    rl.readBeerSmith('/home/mikael/.beersmith2/Cloud.bsmx')
    print "==================Write'm out====================="
    rl.printAll()
