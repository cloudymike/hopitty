#!/usr/bin/python
import pickle
import cgi
import cgitb
import time
import sys

import memcache
#@PydevCodeAnalysisIgnore


def getControllerList(stages):
    controllerList = []
    for stage, step in sorted(stages.items()):
        for ctrl, val in step.items():
            if ctrl not in controllerList:
                controllerList.append(ctrl)
    return(controllerList)


def getListFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    recipeNameList = mc.get(key)
    return(recipeNameList)


def stageStatusMain():
    stages = getListFromMemcache('stagesDict')
    if stages == None:
        stages = {}
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    status = mc.get("hopitty_run_key")
    try:
        currentStage = status['stage']
    except:
        currentStage = ""

    """
    This is an example file, reading some useful value in a recipe file
    Mostly for debugging
    """
    cgitb.enable()

    print "Content-Type: text/html"
    print
    print '<META HTTP-EQUIV="REFRESH" CONTENT="1">'
    print """\
    <html>
    <body>
    <h1>List of stages in current recipe</h1>
    """
    print '<table border="1"><tr>'
    print '<td><b> Stage </td></b>'
    ctrlList = getControllerList(stages)
    for c in ctrlList:
        print "<th>", c, "</th>"
    print '</tr>'
    for stage, step in sorted(stages.items()):
        if stage == currentStage:
            print """<tr style="background-color:green;color:white;">"""
        else:
            print """<tr style="background-color:white;color:black;">"""
        print "<td>", stage, "</td>"
        for c in ctrlList:
            if step[c]['active']:
                print "<td>", step[c]['targetValue'], "</td>"
            else:
                print "<td> </td>"
        print "</tr>"
    print "</table>"
    print '<br><br>'
    print '<a href="/index.html"><button>Home</button></a>'
    print '<a href="status.py"><button>Status</button></a>'
    print """\
    </body>
    </html>
    """

if __name__ == "__main__":
    stageStatusMain()
