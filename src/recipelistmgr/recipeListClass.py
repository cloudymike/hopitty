"""
Handles recipe collection as objects
Reading from bsmx also included
To be used by other modules, including web server
"""

import pickle
import xml.dom.minidom
import ctrl
import recipelistmgr
import recipeReader
import dataMemcache


class recipeListClass():
    def __init__(self, key=None):
        self.list = {}

    def newRecipe(self, name):
        self.list[name] = recipelistmgr.recipeClass(name)
        return(self.list[name])

    def getlist(self):
        return(self.list)

    def getRecipe(self, name):
        try:
            recipe = self.list[name]
        except:
            recipe = None
        return recipe

    def deleteRecipe(self, name):
        del self.list[name]

    def printNameList(self):
        """ Writes a list of all the recipe names"""
        for key, recipe in self.list.items():
            print key

    def nameListToMemcache(self):
        """ A list of all the recipe names to memcache"""
        nameList = []
        for key, recipe in self.list.items():
            nameList.append(key)

        myData = dataMemcache.brewData()
        myData.setRecipeList(nameList)

    def printAll(self):
        """ Writes a list of all the recipe names"""
        for key, recipe in self.list.items():
            print key
            recipe.printRecipeInfo()

    def readBMXdoc(self, doc):
        cloudRecipes = doc.getElementsByTagName("Cloud")
        for recipe in cloudRecipes:
            name = recipeReader.bsmxReadString(recipe, "F_R_NAME")
            r = self.newRecipe(name)
            r.readBMXdoc(recipe)
            #r.setEquipment(ctrl.bsmxReadString(recipe, "F_E_NAME"))

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

    def len(self):
        return (len(self.list))

    def removeBadRecipesList(self, controller):
        deleteList = []
        for key, recipeObject in self.list.items():
            recipeBSMX = recipeObject.getBSMXdoc()
            if not self.runner.checkBSMX(recipeBSMX):
                deleteList.append(recipeName)
        for deleteName in deleteList:
            self.rl.deleteRecipe(deleteName)

        self.rl.nameListToMemcache()
