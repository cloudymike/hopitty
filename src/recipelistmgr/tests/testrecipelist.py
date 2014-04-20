import os
import recipelistmgr
import types
import xml.dom.minidom


def recipeEquivalence(recipe1, recipe2):
    assert recipe1.getName() == recipe2.getName()


def listEquivalence(list1, list2):
    assert len(list1.list) == len(list2.list)


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
    rl = recipelistmgr.recipeListClass()
    doc = xml.dom.minidom.parseString(simpleBsmx())
    rl.readBMXdoc(doc)
    rl.printNameList()
    return(rl)


def getTestRecipeList():
    """ Get recipe list in test directory, and return a recipe list"""
    rl = recipelistmgr.recipeListClass()
    #cp = os.getcwd()
    cp = os.path.dirname(__file__)
    filename = cp + '/../../tests/Cloud.bsmx'
    print filename
    try:
        rl.readBeerSmith(filename)
        print "Right first time"
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
                    print "Could not find test file"
                    print os.getcwd()
    return(rl)


def testMini():
    """ Do a check that recipe list read in is a valid set of recipes
        Be thorough, as all other check are compared against the original
        list.
    """

    rl = getSimpleBSMX()
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


def test_checkType():
    """
    Return a stages list from the recipe named
    """
    rl = getSimpleBSMX()
    for name, recipe in rl.list.items():
        print type(recipe)


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
    testMini()
    print ".........mini done......."
    test_getStages()
    testReading()
    testEqualCheck()
