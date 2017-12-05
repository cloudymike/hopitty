import json
import random

def apipath(appliance):
    print('appliance: ', appliance)

    if appliance == 'boiler':
        actual = random.randint(170,212)
        target = 205
        active = False
    else:
        actual = random.randint(70,170)
        target = 168
        active = True

    targetMet = actual >= target
    powerOn = active and (not targetMet)
    tempJson = {"actual": actual,"target":target,"unit":"F","active":active,"targetMet":targetMet, "powerOn":powerOn}
    return(tempJson)
