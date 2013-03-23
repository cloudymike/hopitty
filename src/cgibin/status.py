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

    if not status:
        try:
            status = pickle.load(open("/tmp/status.pkl", "r"))
        except:
            status = {}
            status['controllers'] = {}
            status['runStop'] = 'Unknown'
            status['watchDog'] = 0
            status['stage'] = 'Unknown'
            status['name'] = 'Unknown'

    controllers = status['controllers']

    common.header("Brew Stages", True)

    print """<h2>%s</h2>""" % status['name']
    print """<h3>Stage: %s</h3>""" % status['stage']

    print """\
    <table border="1">
    <tr>
    <td><b>Controller</td>
    <td><b>Active</td>
    <td><b>Set Value</td>
    <td><b>Actual Value</td>
    <td><b>Power</td>
    <td><b>Done</td>
    </tr>
    """
    for key, c in controllers.items():
        if c['active']:
            print """<tr style="background-color:green;color:white;">"""
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

#dict_.get('key2', "Key doesn't exist")

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


if __name__ == "__main__":
    statusMain()