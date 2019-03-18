import json
import random
import time

def apipath(appliance):

    if appliance == 'boiler':
        actual = random.randint(170,212)
        target = 205
        active = (int((time.time() / 10 )% 2) == 0)
    elif 'Volume' in appliance:
        actual = random.randint(0,12)
        target = 8
        active = (int((time.time() / 10 )% 2) == 0)
        
    else:
        actual = random.randint(70,170)
        target = 168
        active = (int((time.time() / 10 )% 2) == 1)

    print('appliance: ', appliance, 'value: ', actual)

    targetMet = actual >= target
    powerOn = active and (not targetMet)
    tempJson = {"actual": actual,"target":target,"unit":"F","active":active,"targetMet":targetMet, "powerOn":powerOn}
    return(tempJson)

def currentStage():
    # Emulate this:
    # stage = s2b.getStage()
    sixstages = [
        "0 heat water",
        "1 mash in",
        "2 mash",
        "3 sparge",
        "4 boil",
        "5 cool"
        ]
    stno = int((time.time() / 10 )% 6)
    stage = sixstages[stno]
    tmpJson = {"stage": stage}
    return(tmpJson)
