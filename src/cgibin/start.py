#!/usr/bin/python
import pickle
import cgi
import cgitb
import time
import sys

import memcache
#@PydevCodeAnalysisIgnore

import commonweb

DEBUG = False


def objectFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    pickledObject = mc.get(key)
    object = pickle.loads(pickledObject)
    return(object)


def getListFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    recipeNameList = mc.get(key)
    return(recipeNameList)


def getCurrentRecipeFromMemcache():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    try:
        stat = mc.get('hopitty_run_key')
        recipe = stat['name']
    except:
        if DEBUG:
            try:
                recipe = mc.get('currentRecipe')
            except:
                recipe = ""
        else:
            recipe = ""
    return(recipe)


# Use this in final production
def getCurrentStatusRecipeFromMemcache():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    try:
        recipe = mc.get('hopitty_run_key')
    except:
        recipe = ""
    return(recipe)


# Use this in final production
def getRunStatusFromMemcache():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    try:
        runStatus = mc.get('runStatus')
    except:
        runStatus = ""
    return(runStatus)


def getStageFromMemcache():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    status = mc.get("hopitty_run_key")
    try:
        currentStage = status['stage']
    except:
        currentStage = ""
    return(currentStage)


def startMain():
    """
    Page to set the run status, i.e. to start the run
    Also prints some useful info about current status
    """
    common = commonweb.commonweb()
    cgitb.enable()

    print "Content-Type: text/html"
    print
    print """\
    <html>
    <body>
    <h1>Run Control</h1>
    """

    print "Current Recipe: ", getCurrentRecipeFromMemcache(), '<br>'
    print "Current Stage: ", getStageFromMemcache(), '<br>'
    runStatus = getRunStatusFromMemcache()
    print "Run status: ", runStatus, '<br>'
    print '<form method="get" action="startreader.py">'
    if runStatus != 'run':
        print '<input type="hidden" name="runStatus" value="run">'
    print '<input type="submit"'
    if runStatus == 'run':
        print """
        style="color: grey; background-color: white; font-size: larger;
        height:50px;width:80px;"
        """
    else:
        print """
        style="color: white; background-color: green; font-size: larger;
        height:50px;width:80px;"
        """
    print ' value="Start">'

    print '</form>'

    common.pagelinks(__file__)
    print """\
    </body>
    </html>
    """


if __name__ == "__main__":
    startMain()
