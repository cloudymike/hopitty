import json
import random

def apitest():
    temp = random.randint(66,212)
    tempJson = {"hwt": temp}
    return(tempJson)
