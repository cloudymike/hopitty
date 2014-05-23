import os
import recipeReader
import inspect
import xml.dom.minidom
import sys
import ctrl
import recipeModel
import types


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


def elaborateBsmx():
    retval = """
<Recipes>
 <Name>Recipes</Name>
 <Data>
  <Recipe>
   <F_R_NAME>18 Rune Stone  IPA 2.5G</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
    <F_E_MASH_VOL>640.0000000</F_E_MASH_VOL>
    <F_E_BOIL_VOL>436.7360000</F_E_BOIL_VOL>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
    <F_MH_GRAIN_WEIGHT>116.0000000</F_MH_GRAIN_WEIGHT>
    <F_MH_GRAIN_TEMP>68.0000000</F_MH_GRAIN_TEMP>
   </F_R_MASH>
   <Data>
    <MashStep>
      <F_MS_NAME>Mash In</F_MS_NAME>
      <F_MS_INFUSION>290.0000000</F_MS_INFUSION>
      <F_MS_TUN_ADDITION>6.4000000</F_MS_TUN_ADDITION>
      <F_MS_STEP_TEMP>152.0000000</F_MS_STEP_TEMP>
      <F_MS_STEP_TIME>60.0000000</F_MS_STEP_TIME>
      <F_MS_GRAIN_WEIGHT>116.0000000</F_MS_GRAIN_WEIGHT>
      <F_MS_INFUSION>290.0000000</F_MS_INFUSION>
     </MashStep>
   </Data>
    <Ingredients>
     <Data>
      <Grain>
      </Grain>
      <Hops>
        <F_H_NAME>Columbus (Tomahawk)</F_H_NAME>
        <F_H_TYPE>0</F_H_TYPE>
        <F_H_FORM>0</F_H_FORM>
        <F_H_AMOUNT>1.0000000</F_H_AMOUNT>
        <F_H_BOIL_TIME>60.0000000</F_H_BOIL_TIME>
        <F_H_DRY_HOP_TIME>0.0000000</F_H_DRY_HOP_TIME>
        <F_H_IN_RECIPE>1</F_H_IN_RECIPE>
        <F_H_USE>0</F_H_USE>
      </Hops>
      <Misc>
        <F_M_NAME>Whirlfloc Tablet</F_M_NAME>
        <F_M_TYPE>1</F_M_TYPE>
        <F_M_USE_FOR>Clarity</F_M_USE_FOR>
        <F_M_TEMP_VOL>320.0000000</F_M_TEMP_VOL>
        <F_M_UNITS>13</F_M_UNITS>
        <F_M_AMOUNT>0.5000000</F_M_AMOUNT>
        <F_M_VOLUME>640.0000000</F_M_VOLUME>
        <F_M_USE>0</F_M_USE>
        <F_M_TIME_UNITS>0</F_M_TIME_UNITS>
        <F_M_TIME>15.0000000</F_M_TIME>
        <F_M_IMPORT_AS_WEIGHT>1</F_M_IMPORT_AS_WEIGHT>
        <F_M_IMPORT_UNITS>0</F_M_IMPORT_UNITS>
        <F_ORDER>4</F_ORDER>
      </Misc>
     </Data>
    </Ingredients>
  </Recipe>
 </Data>
</Recipes>
    """
    return(retval)


def ctrlBsmxList():
    retlst = ['wortPump', 'boiler']
    return(retlst)


def txDocFromString(bsmxStr):
    """
    Creates doc from an xml string
    """
    bsmxCleanData = bsmxStr.replace('&', 'AMP')
    return(xml.dom.minidom.parseString(bsmxCleanData))


def myname():
    return(inspect.stack()[1][3])


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


def testSimpleBSMX():
    rl = getSimpleBSMX()
    controllers = ctrlBsmxList()
    assert len(rl.getNameList()) > 0
    print "Number of recipes:", len(rl.getNameList())
    for name in rl.getNameList():
        print "...", name
        recipeObjBsmx = rl.getRecipe(name)
        recipeBSMX = recipeObjBsmx.getBSMXdoc()
        recipeObjParsed = recipeReader.bsmxStages(recipeBSMX, controllers)
        print recipeObjParsed.getEquipment()
        print recipeObjParsed.getStages()

    print myname(), "OK"


def testOneFullBSMX():
    rl = getTestRecipeList()
    controllers = ctrl.setupControllers(False, True, True)
    assert len(rl.getNameList()) > 0
    print "Number of recipes:", len(rl.getNameList())
    recipeObj = rl.getRecipe('17 Falconers Flight IPA')
    recipeBSMX = recipeObj.getBSMXstring()
    print recipeBSMX
    recipeObjParsed = recipeReader.bsmxStages(recipeBSMX, controllers)
    print recipeObjParsed.getEquipment()
    s = recipeObjParsed.getStages()
    assert(s != {})
    assert len(s) > 0
    assert(recipeObjParsed.isValid())

    print myname(), "OK"


if __name__ == "__main__":
    testSimpleBSMX()
    testOneFullBSMX()
    print "=====SUCCESS====="
