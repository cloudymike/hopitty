"""
Handles recipe collection as objects
Reading from bsmx also included
To be used by other modules, including web server
"""

# TODO
# Use defs from controller...

import sys
import ctrl
import recipeReader


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
        self.doc = {}

        # Alternative Data store
        self.recipeDict = {}
        self.recipeDict['equipment'] = None

    def checkPopulation(self):
        for key, val in self.recipeDict.items():
            assert val is not None

    def getValue(self, key, value):
        if key in self.recipeDict:
            self.recipeDict[key] = value
        else:
            print "Error: recipe key "
            sys.exit(1)

    def readBMXdoc(self, doc):
        self.doc = doc
        self.setEquipment(recipeReader.bsmxReadString(doc, "F_E_NAME"))
        self.recipeDict['equipment'] =\
            recipeReader.bsmxReadString(doc, "F_E_NAME")

    def printRecipeInfo(self):
        print "    ", self.getEquipment()
        print "    ", self.recipeDict['equipment']

    def setEquipment(self, equipment):
        self.equipment = equipment

    def getEquipment(self):
        return(self.equipment)

    def getName(self):
        return self.name

    def getBSMXdoc(self):
        return(self.doc)
