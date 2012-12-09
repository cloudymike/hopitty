#import sys
import xml.dom.minidom
#import xml.etree.ElementTree as ET
import ctrl


def bsmxReadString(doc, tagName):
    recipeStringNode = doc.getElementsByTagName(tagName)
    recipeString = recipeStringNode[0].firstChild.nodeValue
    return(recipeString)


def bsmxReadTempF(doc, tagName):
    return(float(bsmxReadString(doc, tagName)))


def bsmxReadTimeMin(doc, tagName):
    return(float(bsmxReadString(doc, tagName)))


def bsmxReadVolQt(doc, tagName):
    return(float(bsmxReadString(doc, tagName)) / 32)


def bsmxReadVolG(doc, tagName):
    return(float(bsmxReadString(doc, tagName)) / 128)


def bsmxReadWeightLb(doc, tagName):
    return(float(bsmxReadString(doc, tagName)) / 16)


def setDict(val):
    t = {}
    t['targetValue'] = val
    t['active'] = True
    return(t)


def stageCtrl(controllers):
    settings = {}
    for c_key, c in controllers.items():
        s = {}
        s['targetValue'] = 0
        s['active'] = False
        settings[c_key] = s
    return(settings)


def bsmxReadRecipe(bsmxFile, controllers):
    bsmxFD = open(bsmxFile)
    bsmxRawData = bsmxFD.read()
    bsmxFD.close()

    bsmxCleanData = bsmxRawData.replace('&', 'AMP')
    doc = xml.dom.minidom.parseString(bsmxCleanData)

    # TODO if Mash Method ==
    stages = {}
    # recipe = bsmxReadString(doc, "F_R_NAME")

    s1 = stageCtrl(controllers)
    s1["waterHeater"] = setDict(bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = setDict(1)
    stages["01 Heating"] = s1

    s2 = stageCtrl(controllers)
    s2["delayTimer"] = setDict(0.30)
    stages["02 Pump rest"] = s2

    s3 = stageCtrl(controllers)
    strikeVolNet = bsmxReadVolQt(doc, "F_MS_INFUSION")
    deadSpaceVol = bsmxReadVolQt(doc, "F_MS_TUN_ADDITION")
    strikeVolTot = strikeVolNet + deadSpaceVol
    s3["hotWaterPump"] = setDict(strikeVolTot)
    stages["03 StrikeWater"] = s3

    s4 = stageCtrl(controllers)
    s4["delayTimer"] = setDict(bsmxReadTimeMin(doc, "F_MS_STEP_TIME"))
    s4["waterHeater"] = setDict(bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s4["waterCirculationPump"] = setDict(1)
    stages["04 Mashing"] = s4

    s5 = stageCtrl(controllers)
    grainAbsorption = bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT") / 8.3 * 4
    preboilVol = bsmxReadVolQt(doc, "F_E_BOIL_VOL")
    s5["hotWaterPump"] = setDict(preboilVol / 2 + grainAbsorption - \
                         strikeVolTot)
    stages["05 Sparge in 1"] = s5

    s6 = stageCtrl(controllers)
    s6["waterHeater"] = setDict(bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s6["waterCirculationPump"] = setDict(1)
    s6["mashCirculationPump"] = setDict(1)
    s6["delayTimer"] = setDict(2)
    stages["06 Mash recirculate"] = s6

    s7 = stageCtrl(controllers)
    s7["waterHeater"] = setDict(bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s7["waterCirculationPump"] = setDict(1)
    s7["wortPump"] = setDict(preboilVol / 2)
    stages["07 Wort out 1"] = s7

    s8 = stageCtrl(controllers)
    s8["hotWaterPump"] = setDict(preboilVol / 2)
    stages["08 Sparge in 2"] = s8

    s9 = stageCtrl(controllers)
    s9["waterHeater"] = setDict(bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s9["waterCirculationPump"] = setDict(1)
    s9["mashCirculationPump"] = setDict(1)
    s9["delayTimer"] = setDict(2)
    stages["09 Mash recirculate"] = s9

    s10 = stageCtrl(controllers)
    s10["wortPump"] = setDict(preboilVol / 2)
    stages["10 Wort out 2"] = s10

    return(stages)


def prettyPrintStages(stages):
    for stage, step in sorted(stages.items()):
        print stage
        for ctrl, val in step.items():
            if val['active']:
                print "    ", ctrl, ":", val['targetValue']


def notworkingest_bsmxReader():
    """
    This is the beginning of a test file, not working yet though....
    """
    filename = "../../beersmith/anchor-porter-clone.bsmx"
    c = ctrl.controllerList()
    c.load()
    myStages = bsmxReadRecipe(filename, c)
    assert len(myStages) > 6
    assert ctrl.checkRecipe(c, myStages, True)


def printSomeBsmx(filename):
    """
    This is an example file, reading some useful value in a recipe file
    Mostly for debugging
    """
    bsmxFD = open(filename)
    bsmxRawData = bsmxFD.read()
    bsmxFD.close()

    bsmxCleanData = bsmxRawData.replace('&', 'AMP')
    doc = xml.dom.minidom.parseString(bsmxCleanData)

    print "Recipe:", bsmxReadString(doc, "F_R_NAME")

    equipmentName = bsmxReadString(doc, "F_E_NAME")
    print "Equipment:", equipmentName
    validEquipment = [
                    'Pot and Cooler ( 5 Gal/19 L) - All Grain'
                    ]
    if equipmentName in validEquipment:
        print "Equipment selected is OK"
    else:
        print "Equipment selected is not available"

    print "Infusion temperature:", \
           bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"), "F"

    print "Mash Time:", bsmxReadTimeMin(doc, "F_MS_STEP_TIME"), "min"

    print "Infusion Volume Net:", bsmxReadVolQt(doc, "F_MS_INFUSION"), "qt", \
                                  bsmxReadVolG(doc, "F_MS_INFUSION"), "Gallons"

    infuseVolTot = bsmxReadVolQt(doc, "F_MS_INFUSION") + \
                   bsmxReadVolQt(doc, "F_MS_TUN_ADDITION")
    print "Infusion Volume Total:", infuseVolTot, "qt", \
                                    infuseVolTot / 4, "Gallons"

    mashMethod = bsmxReadString(doc, "F_MH_NAME")
    print "Mash method:", mashMethod
    validMethods = [
                    'Single Infusion, Light Body, Batch Sparge',
                    'Single Infusion, Medium Body, Batch Sparge',
                    'Single Infusion, Full Body, Batch Sparge'
                    ]
    if mashMethod in validMethods:
        print "Mash Method OK"
    else:
        print "Mash Method not supported"

    print "Sparge Temperature:", bsmxReadTempF(doc, "F_MH_SPARGE_TEMP")
    preboilVol = bsmxReadVolQt(doc, "F_E_BOIL_VOL")
    print "Est Pre-boil volume:", preboilVol, 'qt,', preboilVol / 4, 'Gal'

    print "Grain weight: ", bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT"), "lb"

    grainAbsorption = bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT") / 8.3 * 4
    print "Grain absorption:", grainAbsorption, "qt", \
                               grainAbsorption / 4, "Gallons"

    sparge1 = preboilVol / 2 + grainAbsorption - infuseVolTot
    sparge2 = preboilVol / 2
    print "Sparge volume 1:", sparge1, "qt", sparge1 / 4, "Gallons"
    print "Sparge volume 2:", sparge2, "qt", sparge2 / 4, "Gallons"

    boilVol1 = bsmxReadVolQt(doc, "F_MS_TUN_ADDITION") - grainAbsorption
    boilVol2 = sparge1
    boilVol3 = sparge2
    print "Boiler pump1", boilVol1, "qt", boilVol1 / 4, "Gallons"
    print "Boiler pump1", boilVol2, "qt", boilVol2 / 4, "Gallons"
    print "Boiler pump1", boilVol3, "qt", boilVol3 / 4, "Gallons"

    print "Total boil pumped is ", boilVol1 + boilVol2 + boilVol3, "qt", \
           (boilVol1 + boilVol2 + boilVol3) / 4, "Gallons"

if __name__ == "__main__":
    c = ctrl.controllerList()
    c.load()

    #filename = "../../beersmith/SilverDollarPorter.bsmx"
    filename = "../../beersmith/anchor-porter-clone.bsmx"
    #filename = "../../beersmith/barbary-coast-common-beer.bsmx"
    myStages = bsmxReadRecipe(filename, c)
    prettyPrintStages(myStages)
    printSomeBsmx(filename)
