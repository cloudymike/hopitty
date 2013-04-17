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
        else:
            self.bsmxfile = None
            if user == None:
                user = getpass.getuser()
            try:
                self.bsmxfile = "/home/" + user + "/.beersmith2/Cloud.bsmx"
            except:
                print "ERROR: not recipe file"
                sys.exit(1)
        try:
            os.path.isfile(self.bsmxfile)
        except:
            print "ERROR: BSMX file does not exist"
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
        while True:
            self.updateRecipes()
            if run(self.mydata):
                self.runSelectedRecipe()

            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(2)

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
