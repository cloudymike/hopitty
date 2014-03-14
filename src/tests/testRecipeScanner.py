import os
import getpass
import recipelistmgr
import time
import dataMemcache


def getTestRecipeList():
    """ Get recipe list in test directory, and return a recipe list"""
    rl = recipelistmgr.recipeListClass()
    try:
        rl.readBeerSmith('../tests/Cloud.bsmx')
    except:
        try:
            rl.readBeerSmith('./tests/Cloud.bsmx')
        except:
            try:
                rl.readBeerSmith('src/tests/Cloud.bsmx')
            except:
                print "Could not find test file"
                print os.getcwd()
    return(rl)


def testRecipeScanner(user=None):
    if user is None:
        rl = getTestRecipeList()
    else:
        rl = recipelistmgr.recipeListClass()
        bsmxfile = "/home/" + user + "/.beersmith2/Cloud.bsmx"
        rl.readBeerSmith(bsmxfile)
    rl.nameListToMemcache()
    myData = dataMemcache.brewData()
    rl2 = myData.getRecipeList()
    assert rl.len() == len(rl2)
    return(rl)


if __name__ == "__main__":
    user = getpass.getuser()
    print "Getting cloud recipes for", user
    rl = testRecipeScanner(user)
    print rl.len()
