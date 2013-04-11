import xml.dom.minidom
import ctrl
import sys
import mashProfiles


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


def bsmxReadFile(bsmxFile):
    bsmxFD = open(bsmxFile)
    bsmxRawData = bsmxFD.read()
    bsmxFD.close()

    bsmxCleanData = bsmxRawData.replace('&', 'AMP')
    doc = xml.dom.minidom.parseString(bsmxCleanData)
    return(doc)


def bsmxReadName(doc):
    name = bsmxReadString(doc, "F_R_NAME")
    return(name)


def bsmxReadRecipe(doc, controllers):
    """
    Reads the bsmx file and creates a stages list.
    The stages list is created based on Equipment name.
    If no matching Equipemnt name is found, returns None

    Returns None if any error is found and a stages list could not be created
    """

    equipmentName = bsmxReadString(doc, "F_E_NAME")
    print "Equipment:", equipmentName
    validEquipment = [
                    'Pot and Cooler ( 5 Gal/19 L) - All Grain',
                    'Grain 2.5G, 5Gcooler 4Gpot',
                    'Grain 2.5G, 5Gcooler, 4Gpot'
                    ]
    if equipmentName not in validEquipment:
        print "Equipment selected is not available"
        return(None)

    # recipe = bsmxReadString(doc, "F_R_NAME")
    mashProfile = bsmxReadString(doc, "F_MH_NAME")
    stages = None
    if mashProfile in ['Single Infusion, Light Body, Batch Sparge',
                       'Single Infusion, Medium Body, Batch Sparge',
                       'Single Infusion, Full Body, Batch Sparge'
                       ]:
        #stages = mashProfiles.SingleInfusionBatch(doc, controllers)
        stages = mashProfiles.SingleBatchRecycleMash(doc, controllers)

    if mashProfile in ['Single Infusion, Light Body, No Mash Out',
                       'Single Infusion, Medium Body, No Mash Out',
                       'Single Infusion, Full Body, No Mash Out',
                       ]:
        stages = mashProfiles.MultiBatchRecycleMash(doc, controllers)

    if stages == None:
        print "ERROR could not find a valid mash profile"
    else:
        print "Mashprofile selected:", mashProfile
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

    print "================ Equipment and Mash profile ================"
    equipmentName = bsmxReadString(doc, "F_E_NAME")
    print "Equipment:", equipmentName

    validEquipment = [
                    'Pot and Cooler ( 5 Gal/19 L) - All Grain'
                    ]
    if equipmentName in validEquipment:
        print "Equipment selected is OK"
    else:
        print "Equipment selected is not available"

    mashMethod = bsmxReadString(doc, "F_MH_NAME")
    print "Mash method:", mashMethod
    validMethods = [
                    'Single Infusion, Light Body, Batch Sparge',
                    'Single Infusion, Medium Body, Batch Sparge',
                    'Single Infusion, Full Body, Batch Sparge',
                    'Single Infusion, Medium Body, No Mash Out'
                    ]
    if mashMethod in validMethods:
        print "Mash Method OK"
    else:
        print "Mash Method not supported"

    print "================ Sparge raw data ================"

    print "Infusion temperature:", \
           bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"), "F"

    print "Mash Time:", bsmxReadTimeMin(doc, "F_MS_STEP_TIME"), "min"

    infuseVolNet = bsmxReadVolQt(doc, "F_MS_INFUSION")

    print "Infusion Volume Net:", infuseVolNet, "qt", \
                                  infuseVolNet, "Gallons"

    infuseVolTot = bsmxReadVolQt(doc, "F_MS_INFUSION") + \
                   bsmxReadVolQt(doc, "F_MS_TUN_ADDITION")
    print "Infusion Volume Total:", infuseVolTot, "qt", \
                                    infuseVolTot / 4, "Gallons"
    tunDeadSpace = bsmxReadVolQt(doc, 'F_E_TUN_DEADSPACE')
    print "Tun dead space:", tunDeadSpace, "qt", \
                             tunDeadSpace / 4, "Gallons"

    grainAbsorption = bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT") / 8.3 * 4
    preboilVol = bsmxReadVolQt(doc, "F_E_BOIL_VOL")

    print "Sparge Temperature:", bsmxReadTempF(doc, "F_MH_SPARGE_TEMP")
    print "Est Pre-boil volume:", preboilVol, 'qt,', preboilVol / 4, 'Gal'

    print "Grain weight: ", bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT"), "lb"

    print "Grain absorption:", grainAbsorption, "qt", \
                               grainAbsorption / 4, "Gallons"

    totSparge = preboilVol + grainAbsorption - infuseVolNet
    print "Total Sparge vol:", totSparge, "qt", totSparge / 4, "Gallons"
    print "Pre-boil volume:", preboilVol, "qt", preboilVol / 4, "Gallons"

    print "================ Factor Summary================"
    print "Infusion", infuseVolTot, "qt", infuseVolTot / 4, "Gallons"
    print "Sparge", totSparge, "qt", totSparge / 4, "Gallons"
    print "Loss Grain", grainAbsorption, "qt", grainAbsorption / 4, "Gallons"
    print "Dead Space", tunDeadSpace, "qt", tunDeadSpace / 4, "Gallons"
    print "Boil", preboilVol, "qt", preboilVol / 4, "Gallons"
    print "================ Math check ================"
    print "Vol in +", infuseVolTot + totSparge
    print "Loss -", grainAbsorption - tunDeadSpace
    print "Remainder=", infuseVolTot + totSparge \
                        - grainAbsorption - tunDeadSpace
    print "Pre Boil Volume", preboilVol

    print "================ Batch Sparge ================"
    sparge1 = preboilVol / 2 + grainAbsorption - infuseVolNet
    sparge2 = preboilVol / 2
    print "Sparge volume 1:", sparge1, "qt", sparge1 / 4, "Gallons"
    print "Sparge volume 2:", sparge2, "qt", sparge2 / 4, "Gallons"

    boilVol1 = preboilVol / 2
    boilVol2 = preboilVol / 2
    print "Wort pump1", boilVol1, "qt", boilVol1 / 4, "Gallons"
    print "Wort pump1", boilVol2, "qt", boilVol2 / 4, "Gallons"

    print "Total boil pumped is ", boilVol1 + boilVol2, "qt", \
           (boilVol1 + boilVol2) / 4, "Gallons"

    print "Math Check in", sparge1 + sparge2 + infuseVolTot - \
           grainAbsorption - tunDeadSpace
    print "Math Check out:", boilVol1 + boilVol2

    print "================ Almost Fly Sparge ================"
    print "Inital available wort:", infuseVolTot - grainAbsorption
    flySteps = 8
    flySpargeIn = totSparge / flySteps
    flyWortOut = flySpargeIn
    lastWortOut = preboilVol - (flySteps * flyWortOut)

    if flyWortOut > infuseVolNet - grainAbsorption:
        print "ERROR: First with out step too big"

    print "Steps:", flySteps
    print "Sparge volumes:", flySpargeIn, "qt", flySpargeIn / 4, "Gallons"
    print "Wort volumes:", flyWortOut, "qt", flyWortOut / 4, "Gallons"
    print "Last Wort volumes:", lastWortOut, "qt", lastWortOut / 4, "Gallons"
    print "Math Check in", flySteps * flySpargeIn + infuseVolTot \
           - grainAbsorption - tunDeadSpace
    print "Math Check out:", flySteps * flyWortOut + lastWortOut

if __name__ == "__main__":
    c = ctrl.controllerList()
    c.load()

    #filename = "../../beersmith/SilverDollarPorter.bsmx"
    filename = "../../beersmith/spargetest.bsmx"
    #filename = "../../beersmith/barbary-coast-common-beer.bsmx"
    #printSomeBsmx(filename)

    myStages = bsmxReadRecipe(bsmxReadFile(filename), c)
    prettyPrintStages(myStages)
