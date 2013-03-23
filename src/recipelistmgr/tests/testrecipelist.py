import os
import recipelistmgr
import types


def recipeEquivalence(recipe1, recipe2):
    assert recipe1.getName() == recipe2.getName()


def listEquivalence(list1, list2):
    assert len(list1.list) == len(list2.list)


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


def testEqualCheck():
    """testrecipelist this is testing the test tools, so should pass"""
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
