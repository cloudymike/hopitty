import xml.dom.minidom
import ctrl
import sys
import mashProfiles
import dataMemcache


def bsmxReadString(doc, tagName):
    recipeStringNode = doc.getElementsByTagName(tagName)
    recipeString = recipeStringNode[0].firstChild.nodeValue
    return(recipeString)


def bsmxReadDispenseOld(doc):
    boiltime = bsmxReadString(doc, "F_E_BOIL_TIME")
    addTimes = []

    print "boiltime", boiltime
    # Find hop additions times
    tagName = "F_H_BOIL_TIME"
    additions = doc.getElementsByTagName(tagName)
    for addItem in additions:
        at = addItem.firstChild.nodeValue
        # if at != boiltime:
        addTimes.append(float(at))

    # Find misc additions times
    tagName = "F_M_TIME"
    additions = doc.getElementsByTagName(tagName)
    for addItem in additions:
        at = addItem.firstChild.nodeValue
        # if at != boiltime:
        addTimes.append(float(at))

    dedupedAddTimes = list(set(addTimes))
    dedupedAddTimes.sort(reverse=True)

    print dedupedAddTimes
    return(dedupedAddTimes)


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

    The bulk of this def is moved into mashProfiles, as this is where
    customization is kept.

    Also reads recipe to data store
    """
    bsmxRead2DataStore(doc)

    return(mashProfiles.txBSMXtoStages(doc, controllers))


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


def bsmxReadHops(doc):
    tagName = 'Hops'
    hops = doc.getElementsByTagName(tagName)
    hlist = []
    for hop in hops:
        name = hop.getElementsByTagName("F_H_NAME")[0].firstChild.nodeValue

        boil = hop.getElementsByTagName(
            "F_H_BOIL_TIME")[0].firstChild.nodeValue
        dry = hop.getElementsByTagName(
            "F_H_DRY_HOP_TIME")[0].firstChild.nodeValue
        use = hop.getElementsByTagName("F_H_USE")[0].firstChild.nodeValue
        if use == '0':
            print "Boil", name, boil, "minutes"
            hlist.append(float(boil))
        if use == '1':
            print "Dryhop", name, dry, "days"
    return(hlist)


def returnDispenser(doc, t):
    hlist = bsmxReadDispense(doc)
    i = 1
    for h in hlist:
        a = int(float(t))
        b = int(h)
        if a == b:
            dispenser = 'dispenser' + str(i)
            return(dispenser)
        else:
            i = i + 1
    return('error')


def bsmxHops2Recipe(doc):
    d = dataMemcache.brewData()
    tagName = 'Hops'
    hops = doc.getElementsByTagName(tagName)
    for hop in hops:
        name = hop.getElementsByTagName("F_H_NAME")[0].firstChild.nodeValue
        weight = round(float(hop.getElementsByTagName("F_H_AMOUNT")[0].
                       firstChild.nodeValue), 2)
        boil = hop.getElementsByTagName("F_H_BOIL_TIME")[0].\
            firstChild.nodeValue
        dry = hop.getElementsByTagName("F_H_DRY_HOP_TIME")[0].\
            firstChild.nodeValue
        use = hop.getElementsByTagName("F_H_USE")[0].firstChild.nodeValue
        if use == '0':
            d.addToRecipe(name, weight, returnDispenser(doc, boil))


def bsmxMisc2Recipe(doc):
    d = dataMemcache.brewData()
    tagName = 'Misc'
    misc = doc.getElementsByTagName(tagName)
    for m in misc:
        name = m.getElementsByTagName("F_M_NAME")[0].firstChild.nodeValue

        t = m.getElementsByTagName("F_M_TIME")[0].firstChild.nodeValue
        timeunit = m.getElementsByTagName(
            "F_M_TIME_UNITS")[0].firstChild.nodeValue
        amount = round(float(m.getElementsByTagName(
                       "F_M_AMOUNT")[0].firstChild.nodeValue), 2)
        unit = ""
        use = m.getElementsByTagName("F_M_USE")[0].firstChild.nodeValue
        if timeunit == '0':
            tu = 'minutes'
        if timeunit == '1':
            tu = 'days'

        if use == '0':
            d.addToRecipe(name, amount, returnDispenser(doc, t), unit)


def bsmxGrains2Recipe(doc):
    d = dataMemcache.brewData()
    tagName = 'Grain'
    hops = doc.getElementsByTagName(tagName)
    for hop in hops:
        name = hop.getElementsByTagName("F_G_NAME")[0].firstChild.nodeValue
        weight = round(float(hop.getElementsByTagName("F_G_AMOUNT")[0].
                       firstChild.nodeValue), 2)
        d.addToRecipe(name, weight, 'mashtun')


def bsmxReadMisc(doc):
    tagName = 'Misc'
    ms = doc.getElementsByTagName(tagName)
    mlist = []
    for m in ms:
        name = m.getElementsByTagName("F_M_NAME")[0].firstChild.nodeValue

        t = m.getElementsByTagName("F_M_TIME")[0].firstChild.nodeValue
        unit = m.getElementsByTagName("F_M_TIME_UNITS")[0].firstChild.nodeValue
        use = m.getElementsByTagName("F_M_USE")[0].firstChild.nodeValue
        if unit == '0':
            tu = 'minutes'
        if unit == '0':
            tu = 'days'
        if use == '0':
            print "Boil", name, t, tu
            mlist.append(float(t))
        else:
            print "Other", name, t, tu
    return(mlist)


def bsmxReadDispense(doc):
    addTimes = bsmxReadHops(doc) + bsmxReadMisc(doc)
    dedupedAddTimes = list(set(addTimes))
    dedupedAddTimes.sort(reverse=True)

    print dedupedAddTimes
    return(dedupedAddTimes)


def bsmxRead2DataStore(doc):
    d1 = dataMemcache.brewData()
    d1.clearRecipe()
    bsmxGrains2Recipe(doc)
    bsmxHops2Recipe(doc)
    bsmxMisc2Recipe(doc)


if __name__ == "__main__":
    print "start"
    c = ctrl.controllerList()
    c.load()

    # filename = "../../beersmith/spargetest.bsmx"

    # filename = "../../beersmith/SilverDollarPorter.bsmx"
    # filename = "../../beersmith/barbary-coast-common-beer.bsmx"
    filename = "../../beersmith/29BitterAmerican.bsmx"
    d1 = dataMemcache.brewData()
    d1.clearRecipe()
    print('before')

    # printSomeBsmx(filename)
    doc = bsmxReadFile(filename)
    myStages = bsmxReadRecipe(doc, c)
    # prettyPrintStages(myStages)
    # bsmxReadDispense(doc)
    # bsmxRead2DataStore(doc)
    c = d1.getRecipeContainers()
    for container in c:
        mt = d1.getItemsInContainer(container)
        print "================", container
        print mt

    # print(bsmxReadHops(doc))
    # print(bsmxReadMisc(doc))
    # print(bsmxReadDispense(doc))
    print('after')
