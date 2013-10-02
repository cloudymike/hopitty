#!/usr/bin/python
import pickle
import cgi
import cgitb
import time

import commonweb
import dataMemcache


def yn(status):
    if status:
        return("y")
    else:
        return("n")


def statusMain():
    cgitb.enable()

    common = commonweb.commonweb()
    myData = dataMemcache.brewData()
    status = myData.getStatus()
    stage = myData.getCurrentStage()

    errorState = myData.getError()
    # errorState = False
    highLightColor = """<tr style="background-color:green;color:white;">"""
    if errorState:
        highLightColor = """<tr style="background-color:red;color:white;">"""

    # If there is not status, set some default vals to
    # not break but rather show empty values
    if len(status) == 0:
            status = {}
            status['controllers'] = {}
            status['runStop'] = 'Unknown'
            status['watchDog'] = 0
            status['stage'] = 'Unknown'
            status['name'] = 'Unknown'

    controllers = status['controllers']

    common.header("Brew Status", True)

    print """<h2>%s</h2>""" % myData.getCurrentRecipe()
    print """<h3>Stage: %s</h3>""" % stage

    if myData.getRunStatus() == 'run':
        print """\
        <table border="1">
        <tr>
        <td><b>Controller</b></td>
        <td><b>Active</b></td>
        <td><b>Set Value</b></td>
        <td><b>Actual Value</b></td>
        <td><b>Power</b></td>
        <td><b>Done</b></td>
        </tr>
        """
        for key, c in controllers.items():
            if c['active']:
                print highLightColor
            else:
                print """<tr style="background-color:white;color:gray;">"""
            print """<td> %s </td>""" % key
            print """<td>  %s  </td>""" % yn(c['active'])
            if c['unit'] == None:
                print """<td> </td>"""
                print """<td> </td>"""
            else:
                print """<td> %.2f %s</td>""" % (c['target'], c['unit'])
                print """<td> %.2f %s</td>""" % (c['actual'], c['unit'])
            print """<td> %s </td>""" % yn(c['powerOn'])
            print """<td>%s</td>""" % yn(c['targetMet'])
            print "</tr>"

        print "</table>"
    print "<br>"
    checkwatchdog = int(time.time())
    watchdog = status['watchDog']
    if abs(watchdog - checkwatchdog) > 10:
        print "<h1>Controller Stopped Running</h1>"
    else:
        print "Controller status: ", status['runStop']

#    print """\
#    <form method="get" action="ctrlform.py">
#    <input type="submit" value="Settings">
#    </form>
#    """

    common.footer(__file__)


# This is not a test...This is the real thing..
if __name__ == "__main__":
    md = dataMemcache.brewData()
    statusMain()
