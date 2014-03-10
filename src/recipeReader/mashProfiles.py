"""
These defs translates the BSMX recipe to a recipe dictionary that can be
executed but rununit.run (that translates to def runRecipe)

The def txBSMXtoStages selects the translation def to use based on
BSMX data on the Equipment Name and Mash Profile. If not recipe translation
can be found, return None.

All recipe's will be checked in runscan, and only recipes that
returns a dictionary will be added the the recipe list.
This ensures that only recipes that can be translated can be
selected and executed.

If the recipe can not be created, or an error in input data is found
then return None.

If you like to add another brew schedule, just create a new def describing
the translation, and then add this def as an alternative in txBSMXtoStages,
selected based on the Equipment Name, and the Mash Profile Name.
"""
import parseBSMX
import ctrl
import sys

empty = 0
full = 1
dispenserMax = 4
boilTempConstant = 179
coolTempConstant = 72


def grainAbsorption(doc):
    ga = parseBSMX.bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT") / 8.3 * 4
    return(ga)


def tunDeadSpace(doc):
    return(parseBSMX.bsmxReadVolQt(doc, "F_MS_TUN_ADDITION"))


def strikeVolume(doc):
    strikeVolNet = parseBSMX.bsmxReadVolQt(doc, "F_MS_INFUSION")
    strikeVolTot = strikeVolNet + tunDeadSpace(doc)
    return(strikeVolTot)


def preBoilVolume(doc):
    return(parseBSMX.bsmxReadVolQt(doc, "F_E_BOIL_VOL"))


def spargeVolume(doc):
    strikeVolNet = parseBSMX.bsmxReadVolQt(doc, "F_MS_INFUSION")
    return(preBoilVolume(doc) + grainAbsorption(doc) - strikeVolNet)


def txBSMXtoStages(bsmxObj):
    """
    Reads the bsmx file and creates a stages list.
    The stages list is created based on Equipment name.
    If no matching Equipment name is found, returns None

    Returns None if any error is found and a stages list could not be created
    """
    doc = bsmxObj.getDocTree()
    controllers = bsmxObj.getControllers()
    stages = None
    equipmentName = bsmxObj.getEquipment()
    validEquipment1 = ['Pot and Cooler ( 5 Gal/19 L) - All Grain',
                       'Grain 2.5G, 5Gcooler 4Gpot',
                       'Grain 2.5G, 5Gcooler, 4Gpot',
                       'Grain 3G, 5Gcooler, 5Gpot',
                       'Grain 3G, 5Gcooler 5Gpot']

    if not checkVolBSMX(bsmxObj):
        return(None)

    if equipmentName in validEquipment1:
        mashProfile = bsmxObj.getMashProfile()
        if mashProfile in ['Single Infusion, Light Body, Batch Sparge',
                           'Single Infusion, Medium Body, Batch Sparge',
                           'Single Infusion, Full Body, Batch Sparge']:

            stages = SingleInfusionBatch(doc, controllers)

        elif mashProfile in ['Single Infusion, Light Body, No Mash Out',
                             'Single Infusion, Medium Body, No Mash Out',
                             'Single Infusion, Full Body, No Mash Out']:
            stages = MultiBatchMash(doc, controllers)
        elif mashProfile in ['testonly']:
            stages = onlyTestMash(doc, controllers)
        else:
            print "No valid mash profile found"
            print "===", mashProfile, "==="
        if stages is None:
            print "Mash test failed"

    else:
        print ":", equipmentName, ":Not valid equipment"
    return(stages)


def checkVolBSMX(bsmxObj):
    doc = bsmxObj.getDocTree()
    maxInfusionVol = 18  # quarts, before it goes below heater element
    maxTotalInVol = 26  # quarts, before it goes below out spigot
    tunDeadSpaceMin = 0.19
    boilerVolumeMax = 17
    maxTotalWeight = 50 - 5.2 - 1.5 - 1  # 50lb minus mashtun and margin (1lb)

    # return(True)
    # Check tunDead Space
    if tunDeadSpace(doc) < tunDeadSpaceMin:
        print "Error: Tun dead space:", tunDeadSpace(doc), "requires:", \
            tunDeadSpaceMin, "qt"
        return(False)

    # Check boiler volume
    if preBoilVolume(doc) > boilerVolumeMax:
        print "Error: ", preBoilVolume(doc), "exceeding boiler volume"
        return(False)

    if strikeVolume(doc) > maxInfusionVol:
        print "Error: ", strikeVolume(doc), "exceeding infusions volume"
        return(False)

    totInVol = strikeVolume(doc) + spargeVolume(doc)
    if totInVol > maxTotalInVol:
        print "Error: ", totInVol, "exceeding total in volume"
        return(False)

    outLoss = grainAbsorption(doc) + tunDeadSpace(doc) + preBoilVolume(doc)

    inV = round(totInVol, 4)
    outV = round(outLoss, 4)

    if inV != outV:
        print "Deadspace", tunDeadSpace(doc)
        print "Error: In and outvolume mismatch"
        print "In volume ", totInVol, "qt"
        print "Out Volume", outLoss, "qt"
        return(False)

    grainWeight = parseBSMX.bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT")
    fluidWeight = strikeVolume(doc) * 2.08
    totWeight = grainWeight + fluidWeight
    if totWeight > maxTotalWeight:
        print "Total weight ", totWeight, "exceeding max", maxTotalWeight
        return(False)
    return(True)


# Cooling down the worth
def cooling(doc, controllers, stageCount, coolTemp):
    stages = {}
    stageCount = stageCount + 1

    # Cool down the wort to cool temperature
    # Keep going for at least 20 minutes or to cooling
    # temp
    step = parseBSMX.stageCtrl(controllers)
    step["cooler"] = parseBSMX.setDict(coolTemp)
    stages[mkSname("cool", stageCount)] = step
    stageCount = stageCount + 1

    # Hold a  minute to recharge switch
    # We should be done now but in case we are wrong on temperature
    # we will just keep cooling after this step.
    step = parseBSMX.stageCtrl(controllers)
    # step["boiler"] = parseBSMX.setDict(0)
    step["delayTimer"] = parseBSMX.setDict(1)
    stages[mkSname("re-charge", stageCount)] = step
    stageCount = stageCount + 1

    # Open the valve
    # Keep on cooling
    # Keep this stage in essence forever
    step = parseBSMX.stageCtrl(controllers)
    step["cooler"] = parseBSMX.setDict(coolTemp - 40)
    step["delayTimer"] = parseBSMX.setDict(60)
    step["boilerValve"] = parseBSMX.setDict(1)
    stages[mkSname("Empty out", stageCount)] = step
    stageCount = stageCount + 1

    return(stages)


# Bring the pot to boil
# Boil for the suitable time
# Add hops and other additions with the dispensers
# at suitable times.
def boiling(doc, controllers, stageCount, boilTemp):
    stages = {}
    stageCount = stageCount + 1
    print "boiling start"
    # This step is just bringing up temperature to preboil
    # by checking the temperature
    # So no delay required
    step = parseBSMX.stageCtrl(controllers)
    step["boiler"] = parseBSMX.setDict(boilTemp - 5)
    stages[mkSname("pre-boil", stageCount)] = step
    stageCount = stageCount + 1

    print "preboiling done"
    # hold a  few min just below boil to let foam settle
    # Turn off boiler to let things settle
    step = parseBSMX.stageCtrl(controllers)
    # step["boiler"] = parseBSMX.setDict(0)
    step["delayTimer"] = parseBSMX.setDict(1)
    stages[mkSname("de-foam", stageCount)] = step
    stageCount = stageCount + 1

    step = parseBSMX.stageCtrl(controllers)
    step["boiler"] = parseBSMX.setDict(boilTemp)
    stages[mkSname("start boil", stageCount)] = step
    stageCount = stageCount + 1

    boilTime = parseBSMX.bsmxReadTimeMin(doc, "F_E_BOIL_TIME")
    dispenseTimeList = parseBSMX.bsmxReadDispense(doc)

    if len(dispenseTimeList) > 0:
        for dispenseTime in dispenseTimeList:
            if dispenseTime > boilTime:
                # print "ERROR: bad dispense time"
                return(None)

    if len(dispenseTimeList) > 0:

        bt2 = boilTime
        dispenser = 0
        for dispenseTime in dispenseTimeList:
            bt1 = bt2 - dispenseTime
            bt2 = dispenseTime
            step = parseBSMX.stageCtrl(controllers)
            step["delayTimer"] = parseBSMX.setDict(bt1)
            step["boiler"] = parseBSMX.setDict(boilTemp)

            if dispenser > 0:
                dispenserDevice = "dispenser%d" % (dispenser)
                step[dispenserDevice] = parseBSMX.setDict(empty)
                print "================", bt1, dispenserDevice

            stages[mkSname("Boil", stageCount)] = step
            stageCount = stageCount + 1
            dispenser = dispenser + 1

        print "================", bt2, dispenserDevice

        step = parseBSMX.stageCtrl(controllers)
        step["delayTimer"] = parseBSMX.setDict(bt2)
        step["boiler"] = parseBSMX.setDict(boilTemp)
        dispenserDevice = "dispenser%d" % (dispenser)
        step[dispenserDevice] = parseBSMX.setDict(empty)
        stages[mkSname("Boil", stageCount)] = step
        stageCount = stageCount + 1

    else:
        step = parseBSMX.stageCtrl(controllers)
        step["delayTimer"] = parseBSMX.setDict(boilTime)
        step["boiler"] = parseBSMX.setDict(boilTemp)
        stages[mkSname("Boil", stageCount)] = step
        stageCount = stageCount + 1

    step = parseBSMX.stageCtrl(controllers)
    step["delayTimer"] = parseBSMX.setDict(0.1)
    stages[mkSname("Cool down", stageCount)] = step
    stageCount = stageCount + 1

    print "Boiling done"
    return(stages)


def SingleInfusionBatch(doc, controllers):
    print "====================SingleInfusionBatch"
    stages = {}
    s1 = parseBSMX.stageCtrl(controllers)
    s1["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = parseBSMX.setDict(1)
    stages["01 Heating"] = s1

    s2 = parseBSMX.stageCtrl(controllers)
    s2["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s2["delayTimer"] = parseBSMX.setDict(0.30)
    stages["02 Pump rest"] = s2

    s3 = parseBSMX.stageCtrl(controllers)
    strikeVolTot = strikeVolume(doc)
    s3["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s3["hotWaterPump"] = parseBSMX.setDict(strikeVolTot)
    stages["03 StrikeWater"] = s3

    s4 = parseBSMX.stageCtrl(controllers)
    s4["delayTimer"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTimeMin(doc, "F_MS_STEP_TIME"))
    s4["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s4["waterCirculationPump"] = parseBSMX.setDict(1)
    s4["mashStirrer"] = parseBSMX.setDict(1)
    stages["04 Mashing"] = s4

    s6 = parseBSMX.stageCtrl(controllers)
    s6["hotWaterPump"] = parseBSMX.setDict(
        preBoilVolume(doc) / 2 +
        grainAbsorption(doc) -
        strikeVolTot)
    stages["06 Sparge in 1"] = s6

    s7 = parseBSMX.stageCtrl(controllers)
    s7["wortPump"] = parseBSMX.setDict(preBoilVolume(doc) / 2)
    s7["boiler"] = parseBSMX.setDict(1)
    stages["07 Wort out 1"] = s7

    s8 = parseBSMX.stageCtrl(controllers)
    s8["hotWaterPump"] = parseBSMX.setDict(preBoilVolume(doc) / 2)
    s8["boiler"] = parseBSMX.setDict(1)
    stages["08 Sparge in 2"] = s8

    s10 = parseBSMX.stageCtrl(controllers)
    s10["wortPump"] = parseBSMX.setDict(preBoilVolume(doc) / 2)
    s10["boiler"] = parseBSMX.setDict(1)
    stages["10 Wort out 2"] = s10

    try:
        stages.update(boiling(doc, controllers, 11, boilTempConstant))
        stageCount = len(stages)
        stages.update(cooling(doc, controllers, stageCount, coolTempConstant))
    except:
        stages = None

    return(stages)


def mkSname(title, number):
    return("%02d %s" % (number, title))


def MultiBatchMash(doc, controllers):
    """
    Multi batch sparging mash
    """
    print "====================MultiBatchMash"
    stages = {}

    totVolIn = 0
    totVolOut = 0

    stageCount = 1

    s1 = parseBSMX.stageCtrl(controllers)
    s1["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = parseBSMX.setDict(1)

    stages[mkSname("Heating", stageCount)] = s1
    stageCount = stageCount + 1

    s2 = parseBSMX.stageCtrl(controllers)
    s2["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s2["delayTimer"] = parseBSMX.setDict(0.30)
    stages[mkSname("Pump rest", stageCount)] = s2
    stageCount = stageCount + 1

    s3 = parseBSMX.stageCtrl(controllers)
    strikeVolTot = strikeVolume(doc)
    s3["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s3["hotWaterPump"] = parseBSMX.setDict(strikeVolTot)
    totVolIn = totVolIn + strikeVolTot
    stages[mkSname("StrikeWater", stageCount)] = s3
    stageCount = stageCount + 1

    mashTime = parseBSMX.bsmxReadTimeMin(doc, "F_MS_STEP_TIME")
    spargeTemp = parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP")

    step = parseBSMX.stageCtrl(controllers)
    step["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    step["waterCirculationPump"] = parseBSMX.setDict(1)
    step["mashStirrer"] = parseBSMX.setDict(1)
    step["delayTimer"] = parseBSMX.setDict(mashTime)
    stages[mkSname("Mashing", stageCount)] = step
    stageCount = stageCount + 1

    infuseVolNet = parseBSMX.bsmxReadVolQt(doc, "F_MS_INFUSION")

    totSparge = spargeVolume(doc)
    spargeSteps = 4
    volSpargeIn = totSparge / spargeSteps
    volWortOut = volSpargeIn
    lastWortOut = preBoilVolume(doc) - (spargeSteps * volWortOut)

    if volWortOut > infuseVolNet - grainAbsorption(doc):
        print "volWothOut failed"
        return(None)

    for i in range(spargeSteps):

        sHold = parseBSMX.stageCtrl(controllers)
        sHold["delayTimer"] = parseBSMX.setDict(1)
        sHold["boiler"] = parseBSMX.setDict(1)
        stages[mkSname("Sparge hold", stageCount)] = sHold
        stageCount = stageCount + 1

        sOut = parseBSMX.stageCtrl(controllers)
        sOut["wortPump"] = parseBSMX.setDict(volWortOut)
        totVolOut = totVolOut + volWortOut
        sOut["boiler"] = parseBSMX.setDict(1)
        stages[mkSname("Wort out", stageCount)] = sOut
        stageCount = stageCount + 1

        sIn = parseBSMX.stageCtrl(controllers)
        sIn["hotWaterPump"] = parseBSMX.setDict(volSpargeIn)
        totVolIn = totVolIn + volSpargeIn
        sIn["boiler"] = parseBSMX.setDict(1)
        stages[mkSname("Sparge in", stageCount)] = sIn
        stageCount = stageCount + 1

    # For final wort out, run multiple steps and rest in between
    # to allow the wort to seep through the mash, as pumping is too
    # fast otherwise.
    finalWortSteps = 2
    for i in range(finalWortSteps):

        sfwHold = parseBSMX.stageCtrl(controllers)
        sfwHold["delayTimer"] = parseBSMX.setDict(1)
        sfwHold["boiler"] = parseBSMX.setDict(1)
        stages[mkSname("Wort Final hold", stageCount)] = sfwHold
        stageCount = stageCount + 1

        sfw = parseBSMX.stageCtrl(controllers)
        sfw["wortPump"] = parseBSMX.setDict(lastWortOut / finalWortSteps)
        sfw["boiler"] = parseBSMX.setDict(1)
        totVolOut = totVolOut + lastWortOut / finalWortSteps
        stages[mkSname("Wort out final", stageCount)] = sfw
        stageCount = stageCount + 1

    try:
        stages.update(boiling(doc, controllers, stageCount, boilTempConstant))
        stageCount = len(stages)
    except:
        print "Boiling profile failed"
        stages = None

    try:
        stages.update(cooling(doc, controllers, stageCount, coolTempConstant))
    except:
        print "Cooling profile failed"
        stages = None

    # Check and balances
    # tunDeadSpace = parseBSMX.bsmxReadVolQt(doc, 'F_E_TUN_DEADSPACE')

    if round(totVolIn, 4) != \
       round(totVolOut + tunDeadSpace(doc) + grainAbsorption(doc), 4):
        print "Error in/out flow not matching"
        print "In vol:", round(totVolIn, 4)
        print "Out Vol:", round(totVolOut, 4)
        print "Grain absorb and dead space:", \
              round(tunDeadSpace(doc) + grainAbsorption(doc), 4)
        stages = None

    return(stages)


# test mash
# Different shortcust to allow for a shorter test cycle
# The boiling temp as example is low (60F)
def onlyTestMash(doc, controllers):
    """
    Testing mash
    """
    print "====================TestingMash"
    stages = {}

    totVolIn = 0
    totVolOut = 0

    stageCount = 1

    s1 = parseBSMX.stageCtrl(controllers)
    s1["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = parseBSMX.setDict(1)

    stages[mkSname("Heating", stageCount)] = s1
    stageCount = stageCount + 1

    s3 = parseBSMX.stageCtrl(controllers)
    strikeVolTot = strikeVolume(doc)
    s3["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s3["hotWaterPump"] = parseBSMX.setDict(strikeVolTot)
    totVolIn = totVolIn + strikeVolTot
    stages[mkSname("StrikeWater", stageCount)] = s3
    stageCount = stageCount + 1

    mashTime = parseBSMX.bsmxReadTimeMin(doc, "F_MS_STEP_TIME")
    spargeTemp = parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP")

    step = parseBSMX.stageCtrl(controllers)
    step["waterHeater"] = parseBSMX.setDict(
        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    step["waterCirculationPump"] = parseBSMX.setDict(1)
    step["mashStirrer"] = parseBSMX.setDict(1)
    step["delayTimer"] = parseBSMX.setDict(mashTime)
    stages[mkSname("Mashing", stageCount)] = step
    stageCount = stageCount + 1

    volSpargeIn = spargeVolume(doc)
    lastWortOut = preBoilVolume(doc) / 2  # Just cut it down a little

    sIn = parseBSMX.stageCtrl(controllers)
    sIn["hotWaterPump"] = parseBSMX.setDict(volSpargeIn)
    totVolIn = totVolIn + volSpargeIn
    sIn["boiler"] = parseBSMX.setDict(1)
    stages[mkSname("Sparge in", stageCount)] = sIn
    stageCount = stageCount + 1

    sfw = parseBSMX.stageCtrl(controllers)
    sfw["wortPump"] = parseBSMX.setDict(lastWortOut)
    sfw["boiler"] = parseBSMX.setDict(1)
    totVolOut = totVolOut + lastWortOut
    stages[mkSname("Wort out final", stageCount)] = sfw
    stageCount = stageCount + 1

    try:
        stages.update(boiling(doc, controllers, stageCount, 60))
        stageCount = len(stages)
    except:
        print "Boiling profile failed"
        stages = None

    try:
        stages.update(cooling(doc, controllers, stageCount, 90))
    except:
        print "Cooling profile failed"
        stages = None

    return(stages)
