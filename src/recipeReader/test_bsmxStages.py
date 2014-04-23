import os
import recipeReader
import inspect
import xml.dom.minidom
import sys
import ctrl


def simpleBsmx():
    retval = """
<Recipes>
 <Name>Recipes</Name>
 <Data>
  <Recipe>
   <F_R_NAME>18 Rune Stone  IPA 2.5G</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Recipe>
 </Data>
</Recipes>
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


def test_init_bsmxStages_string():
    bx = recipeReader.bsmxStages(simpleBsmx(), ctrlBsmxList())
    assert bx.getRecipeName() == "18 Rune Stone  IPA 2.5G"
    doc = bx.getDocTree()
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    assert equipmentName == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getEquipment() == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getStages() == {}
    print myname(), "OK"


def test_init_bsmxStages_file():
    cp = os.path.dirname(__file__)
    print cp
    rp = cp + "/../../beersmith/18RuneStoneIPA.bsmx"
    print rp
    bx = recipeReader.bsmxStages(rp, ctrlBsmxList())
    assert bx.getRecipeName() == "18 Rune Stone  IPA 2.5G"
    doc = bx.getDocTree()
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    assert equipmentName == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getEquipment() == "Grain 2.5G, 5Gcooler, 4Gpot"
    #print bx.getStages()
    assert bx.getStages() != {}
    print myname(), "OK"


def test_init_bsmxStages_doc():
    doc = txDocFromString(simpleBsmx())
    bx = recipeReader.bsmxStages(doc, ctrlBsmxList())
    assert bx.getRecipeName() == "18 Rune Stone  IPA 2.5G"
    doc = bx.getDocTree()
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    assert equipmentName == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getEquipment() == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getStages() == {}
    print myname(), "OK"


def test_getFieldStr():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    v = bx.getFieldStr('F_E_MASH_VOL')
    assert isinstance(v, str) or isinstance(v, unicode)
    assert v == '640.0000000'
    print myname(), "OK"


def test_getVolG():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    v = bx.getVolG('F_E_MASH_VOL')
    assert isinstance(v, float)
    assert abs(v - 5.0) < 0.1
    print myname(), "OK"


def test_getVolQt():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    v = bx.getVolQt('F_E_MASH_VOL')
    assert isinstance(v, float)
    assert abs(v - 20.0) < 0.1
    print myname(), "OK"


def test_getWeightLb():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    w = bx.getWeightLb('F_MH_GRAIN_WEIGHT')
    assert isinstance(w, float)
    assert abs(w - 7.25) < 0.1
    print myname(), "OK"


def test_getTempF():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    t = bx.getTempF('F_MH_GRAIN_TEMP')
    assert isinstance(t, float)
    assert abs(t - 68.0) < 0.1
    print myname(), "OK"


def myname():
    return(inspect.stack()[1][3])


def test_getTimeMin():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    t = bx.getTimeMin('F_MS_STEP_TIME')
    assert isinstance(t, float)
    assert abs(t - 60.0) < 0.1
    print myname(), "OK"


def test_getMashProfile():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    mp = bx.getMashProfile()
    assert isinstance(mp, str) or isinstance(mp, unicode)
    assert mp == 'Single Infusion, Medium Body, No Mash Out'
    print myname(), "OK"


def test_getEquipment():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    e = bx.getEquipment()
    assert isinstance(e, str) or isinstance(e, unicode)
    assert e == 'Grain 2.5G, 5Gcooler, 4Gpot'
    print myname(), "OK"


def test_getGrainAbsorption():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    g = bx.getGrainAbsorption()
    assert isinstance(g, float)
    assert abs(g - 3.49) < 0.01
    print myname(), "OK"


def test_getTunDeadSpace():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    ds = bx.getTunDeadSpace()
    assert isinstance(ds, float)
    assert abs(ds - 0.2) < 0.01
    print myname(), "OK"


def test_getStrikeVolume():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    ds = bx.getStrikeVolume()
    assert isinstance(ds, float)
    assert abs(ds - 9.2625) < 0.01
    print myname(), "OK"


def test_getPreBoilVolume():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    ds = bx.getPreBoilVolume()
    assert isinstance(ds, float)
    assert abs(ds - 13.648) < 0.01
    print myname(), "OK"


def test_getSpargeVolume():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    ds = bx.getSpargeVolume()
    assert isinstance(ds, float)
    assert abs(ds - 8.07947590361) < 0.01
    print myname(), "OK"


def test_getDispense():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    d = bx.getDispense()
    assert isinstance(d, list)
    assert d == [60.0, 15.0]
    print myname(), "OK"


def test_getDispenserAtTime():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    d1 = bx.getDispenserAtTime(60)
    assert isinstance(d1, str)
    assert d1 == 'dispenser1'

    d2 = bx.getDispenserAtTime(15.1)
    assert isinstance(d2, str)
    assert d2 == 'dispenser2'

    d3 = bx.getDispenserAtTime(0.0)
    assert isinstance(d3, str)
    assert d3 == 'error'

    print myname(), "OK"


def test_getMisc():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    m = bx.getMisc()
    assert isinstance(m, list)
    assert m == [15.0]
    print myname(), "OK"


def test_getHops():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    h = bx.getHops()
    assert isinstance(h, list)
    assert h == [60]
    print myname(), "OK"


def test_prettyPrintStages():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    bx.prettyPrintStages()
    print myname(), "OK"


def test_isValid():
    bx = recipeReader.bsmxStages(simpleBsmx(), ctrlBsmxList())
    assert bx.getRecipeName() == "18 Rune Stone  IPA 2.5G"
    assert not bx.isValid()
    cx = recipeReader.bsmxStages(elaborateBsmx(),
                                 ctrl.setupControllers(False, True, True))
    assert not cx.isValid()
    cp = os.path.dirname(__file__)
    print cp
    rp = cp + "/../../beersmith/18RuneStoneIPA.bsmx"
    print rp
    dx = recipeReader.bsmxStages(rp, ctrl.setupControllers(False, True, True))
    assert dx.isValid()
    print myname(), "OK"


if __name__ == "__main__":
    test_isValid()
    test_init_bsmxStages_string()
    test_init_bsmxStages_file()
    test_init_bsmxStages_doc()
    test_getFieldStr()
    test_getVolG()
    test_getVolQt()
    test_getWeightLb()
    test_getTempF()
    test_getTimeMin()
    test_getMashProfile()
    test_getEquipment()
    test_getGrainAbsorption()
    test_getTunDeadSpace()
    test_getStrikeVolume()
    test_getPreBoilVolume()
    test_getSpargeVolume()
    test_getDispense()
    test_getDispenserAtTime()
    test_getMisc()
    test_getHops()
    test_prettyPrintStages()
    print "=====SUCCESS====="
