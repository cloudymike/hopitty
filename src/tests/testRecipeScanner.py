import os
import getpass
import recipeModel.recipeList


def getTestRecipeList():
    """ Get recipe list in test directory, and return a recipe list"""
    rl = recipeModel.recipeList.RecipeList()
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
        rl = recipeModel.recipeList.RecipeList()
        bsmxfile = "/home/" + user + "/.beersmith2/Cloud.bsmx"
        rl.readBeerSmith(bsmxfile)
    assert len(rl.getNameList()) > 0
    return(rl)


if __name__ == "__main__":
    user = getpass.getuser()
    print "Getting cloud recipes for", user
    rl = testRecipeScanner(user)
    print rl.len()
