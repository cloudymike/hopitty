"""
Handles recipe collection as objects
Reading from bsmx also included
To be used by other modules, including web server
"""

# TODO
# Use defs from controller...

import sys
import xml.dom.minidom
#import xml.etree.ElementTree as ET
import types


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
        self.name = name

    def setEquipment(self, equipment):
        self.equipment = equipment

    def getEquipment(self):
        return(self.equipment)

    def getName(self):
        return self.name


class recipeListClass():
    def __init__(self):
        self.list = {}

    def newRecipe(self, name):
        self.list[name] = recipeClass(name)
        return(self.list[name])

    def storeToMemcache(self):
        """ Stores the class data into memcache record """
        pass

    def loadFromMemcache(self):
        """ Loads all data from memcache record """
        pass

    def printNameList(self):
        """ Writes a list of all the recipe names"""
        for key, recipe in self.list.items():
            print key

    def readBeerSmith(self, fileName):
        bsmxFD = open(fileName)
        bsmxRawData = bsmxFD.read()
        bsmxFD.close()

        bsmxCleanData = bsmxRawData.replace('&', 'AMP')
        doc = xml.dom.minidom.parseString(bsmxCleanData)
        cloudRecipes = doc.getElementsByTagName("Cloud")
        for recipe in cloudRecipes:
            name = bsmxReadString(recipe, "F_R_NAME")
            r = self.newRecipe(name)
            r.setEquipment(bsmxReadString(recipe, "F_E_NAME"))


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
    rl = getTestRecipeList()
    assert len(rl.list) > 0
    for name, recipe in rl.list.items():
        assert len(name) > 0
        assert isinstance(name, types.StringTypes)
        assert name == recipe.getName()

        # Checks on each recipe
        assert isinstance(recipe.getEquipment(), types.StringTypes)
        assert len(recipe.getEquipment()) > 0

    #rl.printNameList()
    print "testReading passed"


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

    print "Alive"
    rl = recipeListClass()
    rl.readBeerSmith('/home/mikael/.beersmith2/Cloud.bsmx')
    print "==================Write'm out====================="
    rl.printNameList()
