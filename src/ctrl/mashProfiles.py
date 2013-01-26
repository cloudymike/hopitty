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
    s4["mashCirculationPump"] = parseBSMX.setDict(1)
    stages["04 Mashing"] = s4

    s5 = parseBSMX.stageCtrl(controllers)
    s5["waterHeater"] = parseBSMX.setDict(\
                        parseBSMX.bsmxReadTempF(doc, "F_MH_SPARGE_TEMP"))
    s5["waterCirculationPump"] = parseBSMX.setDict(1)
    s5["mashCirculationPump"] = parseBSMX.setDict(1)
    s5["delayTimer"] = parseBSMX.setDict(2)
    stages["05 Mash recirculate"] = s5

    s6 = parseBSMX.stageCtrl(controllers)
    grainAbsorption = parseBSMX.bsmxReadWeightLb(doc, "F_MS_GRAIN_WEIGHT")\
                      / 8.3 * 4
    preboilVol = parseBSMX.bsmxReadVolQt(doc, "F_E_BOIL_VOL")
    s6["hotWaterPump"] = parseBSMX.setDict(preboilVol / 2 + grainAbsorption - \
                         strikeVolTot)
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
