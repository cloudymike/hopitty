import os
import recipeModel
import types
import xml.dom.minidom
import sys


def recipeEquivalence(recipe1, recipe2):
    assert recipe1.getName() == recipe2.getName()


def listEquivalence(list1, list2):
    assert len(list1.getNameList()) == len(list2.getNameList())


def simpleBsmx():
    retval = """
<Cloud>
 <Name>Cloud</Name>
 <Data>
  <Cloud>
   <F_R_NAME>18 Rune Stone  IPA 2.5G</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Cloud>
  <Cloud>
   <F_R_NAME>19 Great Brew</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Cloud>
 </Data>
</Cloud>
    """
    return(retval)


def getSimpleBSMX():
    """ Get recipe from simpleBSMX, and return a recipe list"""
    rl = recipeModel.RecipeList()
    doc = xml.dom.minidom.parseString(simpleBsmx())

    rl.readBMXdoc(doc)
    rl.printNameList()
    return(rl)


def getTestRecipeList():
    """ Get recipe list in test directory, and return a recipe list"""
    rl = recipeModel.RecipeList()
    #cp = os.getcwd()
    cp = os.path.dirname(__file__)
    filename = cp + '/../../tests/Cloud.bsmx'
    print(filename)
    try:
        rl.readBeerSmith(filename)
        print("Right first time")
    except:
        try:
            rl.readBeerSmith('../tests/Cloud.bsmx')
        except:
            try:
                rl.readBeerSmith('./tests/Cloud.bsmx')
            except:
                try:
                    rl.readBeerSmith('src/tests/Cloud.bsmx')
                except:
                    print("Could not find test file")
                    print(os.getcwd())
    return(rl)


def testMini():
    """ Do a check that recipe list read in is a valid set of recipes
        Be thorough, as all other check are compared against the original
        list.
    """

    rl = getSimpleBSMX()
    assert len(rl.getNameList()) > 0
    print("Number of recipes:", len(rl.getNameList()))
    for name in rl.getNameList():
        assert len(name) > 0
        assert isinstance(name, types.StringTypes)
        print(name)
        recipe = rl.getRecipeByName(name)
        assert name == recipe.getName()

        # Checks on each recipe
        assert isinstance(recipe.getEquipment(), types.StringTypes)
        assert len(recipe.getEquipment()) > 0

    #rl.printNameList()
    print("testReading passed")


def testReading():
    """ Do a check that recipe list read in is a valid set of recipes
        Be thorough, as all other check are compared against the original
        list.
    """
    rl = getTestRecipeList()
    assert len(rl.getNameList()) > 0
    print("Number of recipes:", len(rl.getNameList()))
    for name in rl.getNameList():
        assert len(name) > 0
        assert isinstance(name, types.StringTypes)
        recipe = rl.getRecipeByName(name)
        assert name == recipe.getName()

        # Checks on each recipe
        assert isinstance(recipe.getEquipment(), types.StringTypes)
        assert len(recipe.getEquipment()) > 0

    #rl.printNameList()
    print("testReading passed")


def testDelete():
    """
    Delete one recipe and check it
    """
    rl = getSimpleBSMX()
    assert len(rl.getNameList()) > 0
    before = len(rl.getNameList())
    name = rl.getNameList()[0]
    rl.deleteRecipeByName(name)
    after = len(rl.getNameList())
    assert after == before - 1
    #rl.printNameList()
    print("testDelete passed")


def testBSMX():
    """
    Check that BSMX read works
    """
    rl = getTestRecipeList()
    assert len(rl.getNameList()) > 0
    print("Number of recipes:", len(rl.getNameList()))
    for name in rl.getNameList():
        recipe = rl.getRecipeByName(name)
        recipeBSMX = recipe.getBSMXdoc()
        assert recipeBSMX is not None

    #rl.printNameList()
    print("testBSMX passed")


if __name__ == "__main__":
    """
    This is an example file, reading some useful value in a recipe file
    Mostly for debugging
    """
    testMini()
    testReading()
    testDelete()
    testBSMX()
