"""
This is a test harness to run runbrew in manual mode and manually test
different pages.
"""
from bottle import route, run, template, Bottle, request
import stages2beer
import ctrl
import appliances
import recipeModel
import os
import xml.dom.minidom
import webctrl
import time
import helpers


def timerDict():
    td = {
        "1 stage": {
            "timer": {
                "active": True,
                "targetValue": 1
            }
        }
    }
    return td


def timerCtrl():
    """Instantiate a list of several controllers"""
    ctrl1 = ctrl.controllerList()
    ctrl1.addController('timer', appliances.hoptimer())
    return(ctrl1)


def simpleBsmx():
    retval = """
<Cloud>
 <Name>Cloud</Name>
 <Data>
  <Cloud>
   <F_R_NAME>18 Rune Stone  IPA 2.5G</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Cloud>
  <Cloud>
   <F_R_NAME>19 Great Brew</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Cloud>
 </Data>
</Cloud>
    """
    return(retval)


def getSimpleBSMX():
    """ Get recipe from simpleBSMX, and return a recipe list"""
    rl = recipeModel.RecipeList()
    doc = xml.dom.minidom.parseString(simpleBsmx())
    rl.readBMXdoc(doc)
    rl.printNameList()
    return(rl)


def getTestRecipeList():
    """ Get recipe list in test directory, and return a recipe list"""
    rl = recipeModel.RecipeList()
    #cp = os.getcwd()
    cp = os.path.dirname(__file__)
    filename = cp + '/../../tests/Cloud.bsmx'
    print filename
    try:
        rl.readBeerSmith(filename)
        print "Right first time"
    except:
        try:
            rl.readBeerSmith('../tests/Cloud.bsmx')
        except:
            try:
                rl.readBeerSmith('./tests/Cloud.bsmx')
            except:
                try:
                    rl.readBeerSmith('src/tests/Cloud.bsmx')
                except:
                    print "Could not find test file"
                    print os.getcwd()
    return(rl)


if __name__ == "__main__":
    #brewer = webctrl.runbrew(timerCtrl(), getSimpleBSMX())

    controllers = ctrl.setupControllers(False, True, True)
    r1 = getTestRecipeList()
    brewer = webctrl.runbrew(controllers, r1)
    brewer.startNonBlocking()

    # This has a problem with sqlite running in a separate thread
    #uptime = 60
    #print "Running for ", uptime, " seconds"
    #time.sleep(uptime)
    #brewer.stop()
    #print "Done"
