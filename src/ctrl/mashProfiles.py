import ctrl
import sys
from parseBSMX import *
import parseBSMX


# Each def takes a recipe input and creates a mash profile
# with stages

def SingleInfusionBatch(doc, controllers):
    stages = {}
    s1 = parseBSMX.stageCtrl(controllers)
    s1["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = parseBSMX.setDict(1)
    stages["01 Heating"] = s1

    s2 = parseBSMX.stageCtrl(controllers)
    s2["delayTimer"] = parseBSMX.setDict(0.30)
    stages["02 Pump rest"] = s2

    s3 = parseBSMX.stageCtrl(controllers)
    strikeVolNet = parseBSMX.bsmxReadVolQt(doc, "F_MS_INFUSION")
    deadSpaceVol = parseBSMX.bsmxReadVolQt(doc, "F_MS_TUN_ADDITION")
    strikeVolTot = strikeVolNet + deadSpaceVol
    s3["hotWaterPump"] = parseBSMX.setDict(strikeVolTot)
    stages["03 StrikeWater"] = s3

    s4 = parseBSMX.stageCtrl(controllers)
    s4["delayTimer"] = parseBSMX.setDict(\
                       parseBSMX.bsmxReadTimeMin(doc, "F_MS_STEP_TIME"))
    s4["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s4["waterCirculationPump"] = parseBSMX.setDict(1)
    stages["04 Mashing"] = s4

    s5 = parseBSMX.stageCtrl(controllers)
    s5["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s5["waterCirculationPump"] = parseBSMX.setDict(1)
    s5["mashCirculationPump"] = parseBSMX.setDict(1)
    s5["delayTimer"] = parseBSMX.setDict(2)
    stages["05 Mash recirculate"] = s5

    s6 = parseBSMX.stageCtrl(controllers)
    grainAbsorption = \
      parseBSMX.bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT") / 8.3 * 4
    preboilVol = parseBSMX.bsmxReadVolQt(doc, "F_E_BOIL_VOL")
    s6["hotWaterPump"] = parseBSMX.setDict(preboilVol / 2 + \
                         grainAbsorption - strikeVolTot)
    stages["06 Sparge in 1"] = s6

    s7 = parseBSMX.stageCtrl(controllers)
    s7["wortPump"] = parseBSMX.setDict(preboilVol / 2)
    stages["07 Wort out 1"] = s7

    s8 = parseBSMX.stageCtrl(controllers)
    s8["hotWaterPump"] = parseBSMX.setDict(preboilVol / 2)
    stages["08 Sparge in 2"] = s8

    s10 = parseBSMX.stageCtrl(controllers)
    s10["wortPump"] = parseBSMX.setDict(preboilVol / 2)
    stages["10 Wort out 2"] = s10

    return(stages)


def SingleBatchRecycleMash(doc, controllers):
    """
    Original single mash, but recirculate mash all through mashing
    """
    stages = {}
    stageCount = 1

    s1 = parseBSMX.stageCtrl(controllers)
    s1["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = parseBSMX.setDict(1)
    stages[mkSname("Heating", stageCount)] = s1
    stageCount = stageCount + 1

    s2 = parseBSMX.stageCtrl(controllers)
    s2["delayTimer"] = parseBSMX.setDict(0.30)
    stages[mkSname("Pump rest", stageCount)] = s2
    stageCount = stageCount + 1

    s3 = parseBSMX.stageCtrl(controllers)
    strikeVolNet = parseBSMX.bsmxReadVolQt(doc, "F_MS_INFUSION")
    deadSpaceVol = parseBSMX.bsmxReadVolQt(doc, "F_MS_TUN_ADDITION")
    strikeVolTot = strikeVolNet + deadSpaceVol
    s3["hotWaterPump"] = parseBSMX.setDict(strikeVolTot)
    stages[mkSname("StrikeWater", stageCount)] = s3
    stageCount = stageCount + 1

    s5 = parseBSMX.stageCtrl(controllers)
    s5["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s5["waterCirculationPump"] = parseBSMX.setDict(1)
    s5["mashCirculationPump"] = parseBSMX.setDict(1)
    s5["delayTimer"] = parseBSMX.setDict(2)
    stages[mkSname("Mash Initial Mix", stageCount)] = s5
    stageCount = stageCount + 1

    mixSteps = 4
    mixTime = 1
    mashTime = parseBSMX.bsmxReadTimeMin(doc, "F_MS_STEP_TIME")
    spargeTemp = parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP")

    for i in range(mixSteps):
        step = parseBSMX.stageCtrl(controllers)
        step["delayTimer"] = parseBSMX.setDict((mashTime / mixSteps) - mixTime)
        step["waterHeater"] = parseBSMX.setDict(spargeTemp)
        step["waterCirculationPump"] = parseBSMX.setDict(1)
        stages[mkSname("Mashing", stageCount)] = step
        stageCount = stageCount + 1

        step = parseBSMX.stageCtrl(controllers)
        step["delayTimer"] = parseBSMX.setDict(mixTime)
        step["waterHeater"] = parseBSMX.setDict(spargeTemp)
        step["waterCirculationPump"] = parseBSMX.setDict(1)
        step["mashCirculationPump"] = parseBSMX.setDict(1)
        stages[mkSname("Mash mix", stageCount)] = step
        stageCount = stageCount + 1

    s5 = parseBSMX.stageCtrl(controllers)
    s5["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s5["waterCirculationPump"] = parseBSMX.setDict(1)
    s5["mashCirculationPump"] = parseBSMX.setDict(1)
    s5["delayTimer"] = parseBSMX.setDict(2)
    stages[mkSname("Mash recirculate", stageCount)] = s5
    stageCount = stageCount + 1

    s6 = parseBSMX.stageCtrl(controllers)
    grainAbsorption = parseBSMX.bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT")\
                      / 8.3 * 4
    preboilVol = parseBSMX.bsmxReadVolQt(doc, "F_E_BOIL_VOL")
    s6["hotWaterPump"] = parseBSMX.setDict(preboilVol / 2 + grainAbsorption - \
                         strikeVolTot)
    stages[mkSname("Sparge in 1", stageCount)] = s6
    stageCount = stageCount + 1

    s7 = parseBSMX.stageCtrl(controllers)
    s7["wortPump"] = parseBSMX.setDict(preboilVol / 2)
    stages[mkSname("Wort out 1", stageCount)] = s7
    stageCount = stageCount + 1

    s8 = parseBSMX.stageCtrl(controllers)
    s8["hotWaterPump"] = parseBSMX.setDict(preboilVol / 2)
    stages[mkSname("Sparge in 2", stageCount)] = s8
    stageCount = stageCount + 1

    s10 = parseBSMX.stageCtrl(controllers)
    s10["wortPump"] = parseBSMX.setDict(preboilVol / 2)
    stages[mkSname("Wort out 2", stageCount)] = s10
    stageCount = stageCount + 1

    return(stages)


def mkSname(title, number):
    return("%02d %s" % (number, title))


def MultiBatchRecycleMash(doc, controllers):
    """
    Multi mash, but recirculate mash all through mashing
    """
    stages = {}

    totVolIn = 0
    totVolOut = 0

    stageCount = 1

    s1 = parseBSMX.stageCtrl(controllers)
    s1["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MS_INFUSION_TEMP"))
    s1["waterCirculationPump"] = parseBSMX.setDict(1)
    stages[mkSname("Heating", stageCount)] = s1
    stageCount = stageCount + 1

    s2 = parseBSMX.stageCtrl(controllers)
    s2["delayTimer"] = parseBSMX.setDict(0.30)
    stages[mkSname("Pump rest", stageCount)] = s2
    stageCount = stageCount + 1

    s3 = parseBSMX.stageCtrl(controllers)
    strikeVolNet = parseBSMX.bsmxReadVolQt(doc, "F_MS_INFUSION")
    deadSpaceVol = parseBSMX.bsmxReadVolQt(doc, "F_MS_TUN_ADDITION")
    strikeVolTot = strikeVolNet + deadSpaceVol
    s3["hotWaterPump"] = parseBSMX.setDict(strikeVolTot)
    totVolIn = totVolIn + strikeVolTot
    stages[mkSname("StrikeWater", stageCount)] = s3
    stageCount = stageCount + 1

    step = parseBSMX.stageCtrl(controllers)
    step["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    step["waterCirculationPump"] = parseBSMX.setDict(1)
    step["mashCirculationPump"] = parseBSMX.setDict(1)
    step["delayTimer"] = parseBSMX.setDict(2)
    stages[mkSname("Mash Initial Mix", stageCount)] = step
    stageCount = stageCount + 1

    mixSteps = 4
    mixTime = 1
    mashTime = parseBSMX.bsmxReadTimeMin(doc, "F_MS_STEP_TIME")
    spargeTemp = parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP")

    for i in range(mixSteps):
        step = parseBSMX.stageCtrl(controllers)
        step["delayTimer"] = parseBSMX.setDict((mashTime / mixSteps) - mixTime)
        step["waterHeater"] = parseBSMX.setDict(spargeTemp)
        step["waterCirculationPump"] = parseBSMX.setDict(1)
        stages[mkSname("Mashing", stageCount)] = step
        stageCount = stageCount + 1

        step = parseBSMX.stageCtrl(controllers)
        step["delayTimer"] = parseBSMX.setDict(mixTime)
        step["waterHeater"] = parseBSMX.setDict(spargeTemp)
        step["waterCirculationPump"] = parseBSMX.setDict(1)
        step["mashCirculationPump"] = parseBSMX.setDict(1)
        stages[mkSname("Mash mix", stageCount)] = step
        stageCount = stageCount + 1

    s5 = parseBSMX.stageCtrl(controllers)
    s5["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s5["waterCirculationPump"] = parseBSMX.setDict(1)
    s5["mashCirculationPump"] = parseBSMX.setDict(1)
    s5["delayTimer"] = parseBSMX.setDict(2)
    stages[mkSname("Mash recirculate", stageCount)] = s5
    stageCount = stageCount + 1

    grainAbsorption = parseBSMX.bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT")\
                      / 8.3 * 4
    preboilVol = parseBSMX.bsmxReadVolQt(doc, "F_E_BOIL_VOL")

    infuseVolNet = parseBSMX.bsmxReadVolQt(doc, "F_MS_INFUSION")
    totSparge = preboilVol + grainAbsorption - infuseVolNet

    spargeSteps = 4
    volSpargeIn = totSparge / spargeSteps
    volWortOut = volSpargeIn
    lastWortOut = preboilVol - (spargeSteps * volWortOut)

    if volWortOut > infuseVolNet - grainAbsorption:
        print "ERROR: First with out step too big"
        sys.exit(1)

    for i in range(spargeSteps):
        sOut = parseBSMX.stageCtrl(controllers)
        sOut["wortPump"] = parseBSMX.setDict(volWortOut)
        totVolOut = totVolOut + volWortOut
        stages[mkSname("Wort out", stageCount)] = sOut
        stageCount = stageCount + 1

        sIn = parseBSMX.stageCtrl(controllers)
        sIn["hotWaterPump"] = parseBSMX.setDict(volSpargeIn)
        totVolIn = totVolIn + volSpargeIn
        stages[mkSname("Sparge in", stageCount)] = sIn
        stageCount = stageCount + 1

    s30 = parseBSMX.stageCtrl(controllers)
    s30["wortPump"] = parseBSMX.setDict(lastWortOut)
    totVolOut = totVolOut + lastWortOut
    stages[mkSname("Wort out final", stageCount)] = s30

    # Check and balances
    tunDeadSpace = parseBSMX.bsmxReadVolQt(doc, 'F_E_TUN_DEADSPACE')

    if round(totVolIn, 4) != \
       round(totVolOut + tunDeadSpace + grainAbsorption, 4):
        print "Error in/out flow not matching"
        print "In vol:", round(totVolIn, 4)
        print "Out Vol:", round(totVolOut, 4)
        print "Grain absorb and dead space:", \
              round(tunDeadSpace + grainAbsorption, 4)
        return(None)

    return(stages)
