import json
import random

def apitest():
    temp = random.randint(70,170)
    tempJson = {"hwt": temp, "boiler": temp}
    return(tempJson)
