import json
import random

def apipath(appliance):
    print('apipath: ' + appliance)
    temp = random.randint(70,170)
    tempJson = {appliance: temp}
    return(tempJson)
