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
import logging

empty = 0
full = 1
dispenserMax = 4
boilTempConstant = 200
coolTempConstant = 72
pumpAdjust = 1.6


#################################################
# Helper functions
#################################################
def mkSname(title, number):
    """
    Creates a stages name that is easily sorted by
    adding a number in the beginning.
    """
    return("%02d %s" % (number, title))


def setDict(val):
    """
    Create a dictionary with target value
    """
    t = {}
    t['targetValue'] = val
    t['active'] = True
    return(t)


def stageCtrl(controllers):
    """
    Creates an empty stage to add to the stage list
    """
    settings = {}
    # This is a little clumsy, but during refactoring keep the option of dict
    if isinstance(controllers, dict):
        for c_key, c in controllers.items():
            s = {}
            s['targetValue'] = 0
            s['active'] = False
            settings[c_key] = s
    elif isinstance(controllers, list):
        for c_key in controllers:
            s = {}
            s['targetValue'] = 0
            s['active'] = False
            settings[c_key] = s
    else:
        logging.info("What the heck is controllers?")

    return(settings)

def strikeTemp(bsmxObj, envT):
    """
    Returns the temperature of the mash in water based on the recipe in
    bsmjObj and the environment temperature, that is applied to both
    grain and equipment
    NOTE: This is now replaced with a similar function in parse BSMX
    """
    Mtun = bsmxObj.getWeightLb('F_E_TUN_MASS')
    Ttun = envT
    Mgrain = bsmxObj.getWeightLb('F_MH_GRAIN_WEIGHT')
    Tgrain = envT

    Vtun = bsmxObj.getVolG('F_E_MASH_VOL')
    Qtun = float(bsmxObj.getFieldStr('F_E_TUN_SPECIFIC_HEAT'))

    Vwater = bsmxObj.getStrikeVolume()
    Tmash = bsmxObj.getTempF('F_MS_STEP_TEMP')

    Ffull = 0.39

    Tstrike = (((((Tmash - 32) / 1.8) * (((Mtun / Vtun * Vwater * Ffull)
                * 453.592 * Qtun) + (Mgrain * 453.592 * 0.38) +
                (Vwater * 946.353)) -
        ((Mtun / Vtun * Vwater * Ffull) *
            453.592 * Qtun * ((Ttun - 32) / 1.8)) -
        (Mgrain * 453.592 * 0.38 * ((Tgrain - 32) / 1.8))) /
        (Vwater * 946.353)) * 1.8) + 32

    # Use this for validation and testing
    beersmithTstrike = bsmxObj.getTempF("F_MS_INFUSION_TEMP")
    print "beersmith strike T ", beersmithTstrike
    print "calculated strike T ", Tstrike

    return(Tstrike)




#################################################
# Main function to translate to stages
#################################################
def txBSMXtoStages(bsmxObj):
    """
    Reads the bsmx file and creates a stages list.
    The stages list is created based on Equipment name.
    If no matching Equipment name is found, returns None

    Returns None if any error is found and a stages list could not be created
    """
    stages = None
    equipmentName = bsmxObj.getEquipment()
    validEquipment1 = ['Pot and Cooler ( 5 Gal/19 L) - All Grain',
                       'Grain 2.5G, 5Gcooler 4Gpot',
                       'Grain 2.5G, 5Gcooler, 4Gpot',
                       'Grain 3G, 5Gcooler, 5Gpot',
                       'Grain 3G, 5Gcooler, 5Gpot, platechiller',
                       'Grain 3G, 5Gcooler 5Gpot']

    if equipmentName in validEquipment1:
        mashProfile = bsmxObj.getMashProfile()
        if equipmentName == 'Grain 3G, 5Gcooler, 5Gpot, platechiller':
            chiller = 'plate'
        else:
            chiller = 'immersion'

        if mashProfile in ['Single Infusion, Light Body, Batch Sparge',
                           'Single Infusion, Medium Body, Batch Sparge',
                           'Single Infusion, Full Body, Batch Sparge']:

            stages = SingleInfusionBatch(bsmxObj, chiller)

        elif mashProfile in ['Single Infusion, Light Body, No Mash Out',
                             'Single Infusion, Medium Body, No Mash Out',
                             'Single Infusion, Full Body, No Mash Out']:
            stages = MultiBatchMash(bsmxObj, chiller)
        elif mashProfile in ['testonly']:
            stages = onlyTestMash(bsmxObj, chiller)
        else:
            print "No valid mash profile found"
            print "===", mashProfile, "==="
        if stages is None:
            print "Mash test failed"

    else:
        print ":", equipmentName, ":Not valid equipment"

    if not checkVolBSMX(bsmxObj):
        return(None)

    return(stages)



def checkVolBSMX(bsmxObj):
    maxInfusionVol = 18  # quarts, before it goes below heater element
    maxTotalInVol = 26  # quarts, before it goes below out spigot
    tunDeadSpaceMin = 0.19
    boilerVolumeMax = 17
    maxTotalWeight = 50 - 5.2 - 1.5 - 1  # 50lb minus mashtun and margin (1lb)

    # return(True)
    # Check tunDead Space
    if bsmxObj.getTunDeadSpace() < tunDeadSpaceMin:
        print "Error: Tun dead space:", bsmxObj.getTunDeadSpace(),\
            "requires:", tunDeadSpaceMin, "qt"
        return(False)

    # Check boiler volume
    if bsmxObj.getPreBoilVolume() > boilerVolumeMax:
        print "Error: ", bsmxObj.getPreBoilVolume(), "exceeding boiler volume"
        return(False)

    if bsmxObj.getStrikeVolume() > maxInfusionVol:
        print("Error: ", bsmxObj.getStrikeVolume(),
              "exceeding infusions volume")
        return(False)

    totInVol = bsmxObj.getStrikeVolume() + bsmxObj.getSpargeVolume()
    if totInVol > maxTotalInVol:
        print "Error: ", totInVol, "exceeding total in volume"
        return(False)

    outLoss = bsmxObj.getGrainAbsorption() + bsmxObj.getTunDeadSpace() +\
        bsmxObj.getPreBoilVolume()

    inV = round(totInVol, 4)
    outV = round(outLoss, 4)

    if inV != outV:
        print "Deadspace", bsmxObj.getTunDeadSpace()
        print "Error: In and outvolume mismatch"
        print "In volume ", totInVol, "qt"
        print "Out Volume", outLoss, "qt"
        return(False)

    grainWeight = bsmxObj.getWeightLb("F_MS_GRAIN_WEIGHT")
    fluidWeight = bsmxObj.getStrikeVolume() * 2.08
    totWeight = grainWeight + fluidWeight
    if totWeight > maxTotalWeight:
        print "Total weight ", totWeight, "exceeding max", maxTotalWeight
        return(False)
    return(True)


#################################################
# Functions that are generic to all mashes
#################################################
# Cooling down the worth
def cooling(bsmxObj, stageCount, coolTemp):
    controllers = bsmxObj.getControllers()
    stages = {}
    stageCount = stageCount + 1

    # Cool down the wort to cool temperature
    # Keep going for at least 20 minutes or to cooling
    # temp
    step = stageCtrl(controllers)
    step["cooler"] = setDict(coolTemp)
    stages[mkSname("cool", stageCount)] = step
    stageCount = stageCount + 1

    # Hold a  minute to recharge switch
    # We should be done now but in case we are wrong on temperature
    # we will just keep cooling after this step.
    step = stageCtrl(controllers)
    # step["boiler"] = setDict(0)
    step["delayTimer"] = setDict(1)
    stages[mkSname("re-charge", stageCount)] = step
    stageCount = stageCount + 1

    # Open the valve
    step = stageCtrl(controllers)
    #step["cooler"] = setDict(coolTemp - 40)
    step["delayTimer"] = setDict(15)
    step["boilerValve"] = setDict(1)
    step["aerator"] = setDict(1)
    stages[mkSname("Empty out", stageCount)] = step
    stageCount = stageCount + 1

    # Done
    # shutdown everything
    # Keep this stage in essence forever, well 10h
    step = stageCtrl(controllers)
    #step["cooler"] = setDict(coolTemp - 40)
    step["delayTimer"] = setDict(600)
    #step["boilerValve"] = setDict(0)
    #step["aerator"] = setDict(0)
    stages[mkSname("Done", stageCount)] = step
    stageCount = stageCount + 1

    return(stages)


def plateCooling(bsmxObj, stageCount, coolTemp):
    controllers = bsmxObj.getControllers()
    stages = {}
    stageCount = stageCount + 1

    # Open the valve
    step = stageCtrl(controllers)
    #step["cooler"] = setDict(coolTemp - 40)
    step["delayTimer"] = setDict(7)
    step["boilerValve"] = setDict(1)
    step["aerator"] = setDict(1)
    step["plateValve"] = setDict(1)
    stages[mkSname("Empty out", stageCount)] = step
    stageCount = stageCount + 1

    # Done
    # shutdown everything
    # Keep this stage in essence forever, well 10h
    step = stageCtrl(controllers)
    #step["cooler"] = setDict(coolTemp - 40)
    step["delayTimer"] = setDict(600)
    #step["boilerValve"] = setDict(0)
    #step["aerator"] = setDict(0)
    stages[mkSname("Done", stageCount)] = step
    stageCount = stageCount + 1

    return(stages)


# Bring the pot to boil
# Boil for the suitable time
# Add hops and other additions with the dispensers
# at suitable times.
def boiling(bsmxObj, stageCount, boilTemp):
    doc = bsmxObj.getDocTree()
    controllers = bsmxObj.getControllers()
    stages = {}
    stageCount = stageCount + 1
    logging.info("boiling start")
    # This step is just bringing up temperature to preboil
    # by checking the temperature
    # So no delay required
    step = stageCtrl(controllers)
    step["boiler"] = setDict(boilTemp - 5)
    stages[mkSname("pre-boil", stageCount)] = step
    stageCount = stageCount + 1

    logging.info("preboiling done")
    # hold a  few min just below boil to let foam settle
    # Turn off boiler to let things settle
    step = stageCtrl(controllers)
    # step["boiler"] = setDict(0)
    step["delayTimer"] = setDict(1)
    stages[mkSname("de-foam", stageCount)] = step
    stageCount = stageCount + 1

    step = stageCtrl(controllers)
    step["boiler"] = setDict(boilTemp)
    stages[mkSname("start boil", stageCount)] = step
    stageCount = stageCount + 1

    boilTime = bsmxObj.getTimeMin("F_E_BOIL_TIME")
    dispenseTimeList = bsmxObj.getDispense()

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
            step = stageCtrl(controllers)
            step["delayTimer"] = setDict(bt1)
            step["boiler"] = setDict(boilTemp)

            if dispenser > 0:
                dispenserDevice = "dispenser%d" % (dispenser)
                step[dispenserDevice] = setDict(empty)
                logging.info("================ " +
                             str(bt1) + " " +
                             dispenserDevice)

            stages[mkSname("Boil", stageCount)] = step
            stageCount = stageCount + 1
            dispenser = dispenser + 1

        dispenserDevice = "dispenser%d" % (dispenser)
        logging.info("================ " + str(bt2) + " " + dispenserDevice)

        step = stageCtrl(controllers)
        step["delayTimer"] = setDict(bt2)
        step["boiler"] = setDict(boilTemp)
        dispenserDevice = "dispenser%d" % (dispenser)
        step[dispenserDevice] = setDict(empty)
        stages[mkSname("Boil", stageCount)] = step
        stageCount = stageCount + 1

    else:
        step = stageCtrl(controllers)
        step["delayTimer"] = setDict(boilTime)
        step["boiler"] = setDict(boilTemp)
        stages[mkSname("Boil", stageCount)] = step
        stageCount = stageCount + 1

    step = stageCtrl(controllers)
    step["delayTimer"] = setDict(0.1)
    stages[mkSname("Cool down", stageCount)] = step
    stageCount = stageCount + 1

    steepTime = bsmxObj.getSteepTime()

    if (steepTime > 1):
        steepTemp = boilTemp - 4
        logging.info("Cooling to steep temp " + str(steepTime) + "F")
        step = stageCtrl(controllers)
        step["boiler"] = setDict(steepTemp)
        stages[mkSname("SteepTemp", stageCount)] = step
        stageCount = stageCount + 1
        
        logging.info("Steeping for " + str(steepTime) + " minutes")
        step = stageCtrl(controllers)
        step["delayTimer"] = setDict(steepTime)
        stages[mkSname("Steeping", stageCount)] = step
        stageCount = stageCount + 1

    logging.info("Boiling done")
    return(stages)


#################################################
# Specifics of different types of mashes
#################################################
def SingleInfusionBatch(bsmxObj, chiller):
    controllers = bsmxObj.getControllers()
    logging.info("====================SingleInfusionBatch")
    stages = {}
    s0 = stageCtrl(controllers)
    s0["waterCirculationPump"] = setDict(1)
    s0["delayTimer"] = setDict(3.0)
    stages["00 Pre-circulate"] = s0

    s1 = stageCtrl(controllers)
    s1["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = setDict(1)
    stages["01 Heating"] = s1

    s2 = stageCtrl(controllers)
    s2["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MS_INFUSION_TEMP"))
    s2["delayTimer"] = setDict(0.30)
    stages["02 Pump rest"] = s2

    s3 = stageCtrl(controllers)
    ############################################### First Try
    strikeVolTot = bsmxObj.getStrikeVolume()
    s3["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MS_INFUSION_TEMP"))
    s3["hotWaterPump"] = setDict(strikeVolTot)
    stages["03 StrikeWater"] = s3

    s4 = stageCtrl(controllers)
    s4["delayTimer"] = setDict(
        bsmxObj.getTimeMin("F_MS_STEP_TIME"))
    s4["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MH_SPARGE_TEMP"))
    s4["waterCirculationPump"] = setDict(1)
    s4["mashStirrer"] = setDict(1)
    stages["04 Mashing"] = s4

    s6 = stageCtrl(controllers)
    s6["hotWaterPump"] = setDict(
        bsmxObj.getPreBoilVolume() / 2 +
        bsmxObj.getGrainAbsorption() -
        strikeVolTot)
    stages["06 Sparge in 1"] = s6

    s7 = stageCtrl(controllers)
    s7["wortPump"] = setDict(bsmxObj.getPreBoilVolume() / 2)
    # Do not start boiler until after first fillup
    # In case of pump problems, you may burn the pot
    s7["boiler"] = setDict(0)
    stages["07 Wort out 1"] = s7

    s8 = stageCtrl(controllers)
    s8["hotWaterPump"] = setDict(bsmxObj.getPreBoilVolume() / 2)
    s8["boiler"] = setDict(0)
    stages["08 Sparge in 2"] = s8

    s10 = stageCtrl(controllers)
    s10["wortPump"] = setDict(bsmxObj.getPreBoilVolume() / 2)
    s10["boiler"] = setDict(1)
    stages["10 Wort out 2"] = s10

    try:
        stages.update(boiling(bsmxObj, 11, boilTempConstant))
        stageCount = len(stages)
        if chiller == 'immersion':
            stages.update(cooling(bsmxObj, stageCount, coolTempConstant))
        elif chiller == 'plate':
            stages.update(plateCooling(bsmxObj, stageCount, coolTempConstant))
        else:
            logging.info('Unknown cooler type')
            stages = None
    except:
        stages = None

    return(stages)


def MultiBatchMash(bsmxObj, chiller):
    """
    Multi batch sparging mash
    """
    logging.info("====================MultiBatchMash")
    controllers = bsmxObj.getControllers()
    stages = {}

    totVolIn = 0
    totVolOut = 0

    stageCount = 1

    s0 = stageCtrl(controllers)
    s0["waterCirculationPump"] = setDict(1)
    s0["delayTimer"] = setDict(3.0)
    stages["00 Pre-circulate"] = s0

    s1 = stageCtrl(controllers)
    s1["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = setDict(1)

    stages[mkSname("Heating", stageCount)] = s1
    stageCount = stageCount + 1

    s2 = stageCtrl(controllers)
    s2["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MS_INFUSION_TEMP"))
    s2["delayTimer"] = setDict(0.30)
    stages[mkSname("Pump rest", stageCount)] = s2
    stageCount = stageCount + 1

    s3 = stageCtrl(controllers)
    strikeVolTot = bsmxObj.getStrikeVolume()
    s3["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MS_INFUSION_TEMP"))
    s3["hotWaterPump"] = setDict(strikeVolTot)
    totVolIn = totVolIn + strikeVolTot
    stages[mkSname("StrikeWater", stageCount)] = s3
    stageCount = stageCount + 1

    mashTime = bsmxObj.getTimeMin("F_MS_STEP_TIME")

    step = stageCtrl(controllers)
    step["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MH_SPARGE_TEMP"))
    step["waterCirculationPump"] = setDict(1)
    step["mashStirrer"] = setDict(1)
    step["delayTimer"] = setDict(mashTime)
    stages[mkSname("Mashing", stageCount)] = step
    stageCount = stageCount + 1

    infuseVolNet = bsmxObj.getVolQt("F_MS_INFUSION")

    totSparge = bsmxObj.getSpargeVolume()
    spargeSteps = 4
    volSpargeIn = totSparge / spargeSteps
    volWortOut = volSpargeIn
    lastWortOut = bsmxObj.getPreBoilVolume() - (spargeSteps * volWortOut) - pumpAdjust

    if volWortOut > infuseVolNet - bsmxObj.getGrainAbsorption():
        logging.info("volWothOut failed")
        return(None)

    for i in range(spargeSteps):

        sHold = stageCtrl(controllers)
        sHold["delayTimer"] = setDict(1)

        sOut = stageCtrl(controllers)
        sOut["wortPump"] = setDict(volWortOut)
        totVolOut = totVolOut + volWortOut
        if i < 1:
            sOut["boiler"] = setDict(0)
        else:
            sOut["boiler"] = setDict(1)
        stages[mkSname("Wort out", stageCount)] = sOut
        stageCount = stageCount + 1

        # Do not start boiler until after first fill up
        # In case of pump problems, you may burn the pot
        sHold["boiler"] = setDict(1)
        stages[mkSname("Sparge hold", stageCount)] = sHold
        stageCount = stageCount + 1

        sIn = stageCtrl(controllers)
        sIn["hotWaterPump"] = setDict(volSpargeIn)
        totVolIn = totVolIn + volSpargeIn
        sIn["boiler"] = setDict(1)
        stages[mkSname("Sparge in", stageCount)] = sIn
        stageCount = stageCount + 1

    # For final wort out, run multiple steps and rest in between
    # to allow the wort to seep through the mash, as pumping is too
    # fast otherwise.
    finalWortSteps = 2
    for i in range(finalWortSteps):

        sfwHold = stageCtrl(controllers)
        sfwHold["delayTimer"] = setDict(1)
        sfwHold["boiler"] = setDict(1)
        stages[mkSname("Wort Final hold", stageCount)] = sfwHold
        stageCount = stageCount + 1

        sfw = stageCtrl(controllers)
        sfw["wortPump"] = setDict(lastWortOut / finalWortSteps)
        sfw["boiler"] = setDict(1)
        totVolOut = totVolOut + lastWortOut / finalWortSteps
        stages[mkSname("Wort out final", stageCount)] = sfw
        stageCount = stageCount + 1

    try:
        stages.update(boiling(bsmxObj, stageCount, boilTempConstant))
        stageCount = len(stages)
    except:
        logging.error("Boiling profile failed")
        stages = None

    try:
        if chiller == 'immersion':
            stages.update(cooling(bsmxObj, stageCount, coolTempConstant))
        elif chiller == 'plate':
            stages.update(plateCooling(bsmxObj, stageCount, coolTempConstant))
        else:
            logging.error('Unknown cooler type')
            stages = None
    except:
        logging.error("Cooling profile failed")
        stages = None

    # Check and balances
    # tunDeadSpace = bsmxReadVolQt(doc, 'F_E_TUN_DEADSPACE')

    if round(totVolIn, 4) != \
       round(totVolOut + pumpAdjust + bsmxObj.getTunDeadSpace() +
             bsmxObj.getGrainAbsorption(), 4):
        logging.error("Error in/out flow not matching")
        logging.error("In vol: "+str(round(totVolIn, 4)))
        logging.error("Out Vol: "+str(round(totVolOut, 4)))
        logging.error("Grain absorb and dead space: " +
                      str(round(bsmxObj.getTunDeadSpace() +
                          bsmxObj.getGrainAbsorption(), 4)))
        stages = None

    return(stages)


# test mash
# Different shortcust to allow for a shorter test cycle
# The boiling temp as example is low (60F)
def onlyTestMash(bsmxObj, chiller):
    """
    Testing mash
    """
    logging.info("====================TestingMash")
    controllers = bsmxObj.getControllers()
    stages = {}

    totVolIn = 0
    totVolOut = 0

    stageCount = 1

    s1 = stageCtrl(controllers)
    s1["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = setDict(1)

    stages[mkSname("Heating", stageCount)] = s1
    stageCount = stageCount + 1

    s3 = stageCtrl(controllers)
    strikeVolTot = bsmxObj.getStrikeVolume()
    s3["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MS_INFUSION_TEMP"))
    s3["hotWaterPump"] = setDict(strikeVolTot)
    totVolIn = totVolIn + strikeVolTot
    stages[mkSname("StrikeWater", stageCount)] = s3
    stageCount = stageCount + 1

    mashTime = bsmxObj.getTimeMin("F_MS_STEP_TIME")

    step = stageCtrl(controllers)
    step["waterHeater"] = setDict(
        bsmxObj.getTempF("F_MH_SPARGE_TEMP"))
    step["waterCirculationPump"] = setDict(1)
    step["mashStirrer"] = setDict(1)
    step["delayTimer"] = setDict(mashTime)
    stages[mkSname("Mashing", stageCount)] = step
    stageCount = stageCount + 1

    volSpargeIn = bsmxObj.getSpargeVolume()
    lastWortOut = bsmxObj.getPreBoilVolume() / 2  # Just cut it down a little

    sIn = stageCtrl(controllers)
    sIn["hotWaterPump"] = setDict(volSpargeIn)
    totVolIn = totVolIn + volSpargeIn
    sIn["boiler"] = setDict(1)
    stages[mkSname("Sparge in", stageCount)] = sIn
    stageCount = stageCount + 1

    sfw = stageCtrl(controllers)
    sfw["wortPump"] = setDict(lastWortOut)
    sfw["boiler"] = setDict(1)
    totVolOut = totVolOut + lastWortOut
    stages[mkSname("Wort out final", stageCount)] = sfw
    stageCount = stageCount + 1

    try:
        stages.update(boiling(bsmxObj, stageCount, 60))
        stageCount = len(stages)
    except:
        logging.error("Boiling profile failed")
        stages = None

    try:
        if chiller == 'immersion':
            stages.update(cooling(bsmxObj, stageCount, 90))
        elif chiller == 'plate':
            stages.update(plateCooling(bsmxObj, stageCount, 90))
        else:
            logging.error('Unknown cooler type')
            stages = None
    except:
        logging.error("Cooling profile failed")
        stages = None

    return(stages)
