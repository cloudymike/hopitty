import json
import random
import time


def appliance(s2b, appliance):
    return(s2b.getApplianceStatus(appliance))


def currentStage(s2b):
    tmpJson = {"stage": s2b.getStage()}
    return(tmpJson)
