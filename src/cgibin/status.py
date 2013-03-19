#!/usr/bin/python
import pickle
import cgi
import cgitb
import time
import memcache
#@PydevCodeAnalysisIgnore

import commonweb


def yn(status):
    if status:
        return("y")
    else:
        return("n")


def statusMain():
    common = commonweb.commonweb()
    cgitb.enable()
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    status = mc.get("hopitty_run_key")
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

    print "Content-Type: text/html"
    print
    print '<META HTTP-EQUIV="REFRESH" CONTENT="1">'
    print """\
    <html>
    <body>
    <h1>Brewing Status Display</h1>
    <h2>%s</h2>
    """ % status['name']
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

    print '<br><br>'
    common.pagelinks(__file__)
    print """\
    <form method="get" action="ctrlform.py">
    <input type="submit" value="Settings">
    </form>
    """

    print """\
    </body>
    </html>
    """


if __name__ == "__main__":
    statusMain()
