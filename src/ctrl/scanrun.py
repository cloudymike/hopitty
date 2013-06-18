"""
Scans the recipe database and creates recipeListClass object
Also pushes recipe name list to memcache for use by web pages

"""

import sys
#sys.path.append("/home/mikael/workspace/hoppity/src")
#sys.path.append("/home/mikael/workspace/hoppity/src/recipelistmgr")
import getpass
import os
import recipelistmgr
import time
import ctrl
import dataMemcache
from os import path, access, R_OK  # W_OK for write permission.


def run(mydata):
    rs = mydata.getRunStatus()
    if rs == 'run':
        return(True)
    else:
        return(False)


class scanrun():
    def __init__(self, recipefile=None, user=None):
        self.rl = recipelistmgr.recipeListClass()
        self.mydata = dataMemcache.brewData()
        self.runner = ctrl.rununit()

        # Try to find a recipe file
        if recipefile != None:
            self.bsmxfile = recipefile
        elif user != None:
            self.bsmxfile = "/home/" + user + "/.beersmith2/Cloud.bsmx"
        else:
            print "ERROR: No data for BSMX file"
            sys.exit(1)

        print self.bsmxfile

        if path.isfile(self.bsmxfile) and access(self.bsmxfile, R_OK):
            print "BSMX File", self.bsmxfile, "exists and is readable"
        else:
            print "ERROR: BSMX file", self.bsmxfile,\
                  "is missing or is not readable"
            sys.exit(1)

        self.updateRecipes()
        print "================ Recipe List ==============="
        self.rl.printNameList()
        print "============================================"

    def updateRecipes(self):
        self.rl.readBeerSmith(self.bsmxfile)
        iterlist = self.rl.getlist()
        deleteList = []
        for recipeName in iterlist:
            recipeObject = self.rl.getRecipe(recipeName)
            recipeBSMX = recipeObject.getBSMXdoc()
            if not self.runner.checkBSMX(recipeBSMX):
                deleteList.append(recipeName)
        for deleteName in deleteList:
            self.rl.deleteRecipe(deleteName)

        self.rl.nameListToMemcache()

    def getRecipeList(self):
        self.updateRecipes()
        return(self.rl)

    def loop(self):
        print "starting daemon mode"
        i = 0
        while True:
            # Update recipe list every 60 sec
            # Doing it every second is too expensive
            i = i + 1
            if i == 60:
                self.updateRecipes()
                i = 0

            if run(self.mydata):
                self.runSelectedRecipe()
                print "Stopped recipe"

            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)

    def runSelectedRecipe(self, quick=False):
        """
        Main method, runs the recipe.
        Assumes recipe list is read in, recipe selected and run enabled
        The quick option is rununit.quick, a testing option that is doing
        a run without any delays.
        """
        r = self.rl.getRecipe(self.mydata.getSelectedRecipe())
        if run(self.mydata):
            if r != None:
                bsxml = r.getBSMXdoc()
                self.runner.bsmxIn(bsxml)
                print "+++++++++++++++",\
                     self.runner.getRecipeName(),\
                     "+++++++++++++++"
                if quick:
                    runOK = self.runner.quick()
                else:
                    runOK = self.runner.run()
                if not runOK:
                    print "Run failed"
                self.runner.stop()
                self.mydata.setRunStatus('stop')
            else:
                print "No recipe selected"
        else:
            print "Run not enabled"

    def HWOK(self):
        return(self.runner.HWOK())
