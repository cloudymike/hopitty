#!/usr/bin/python
import pickle
import cgi
import cgitb
import time


def yn(status):
    if status:
        return("y")
    else:
        return("n")

cgitb.enable()
try:
    status = pickle.load(open("/tmp/status.pkl", "r"))
except:
    status = {}
    status['controller'] = {}
    status['runStop'] = 'Unknown'
    status['watchDog'] = 0

controllers = status['controllers']

print "Content-Type: text/html"
print
print '<META HTTP-EQUIV="REFRESH" CONTENT="5">'
print """\
<html>
<body>
<h2>Status</h2>
"""

print """\
<table border="1">
<tr>
<td><b>Controller</td>
<td><b>Set Value</td>
<td><b>Actual Value</td>
<td><b>On</td>
<td><b>Done</td>
</tr>
"""
for key, c in controllers.items():
    print """<tr><td> %s </td>""" % key
    print """<td> %s %s</td>""" % (c['target'], c['unit'])
    print """<td> %s %s</td>""" % (c['actual'], c['unit'])
    print """<td> %s </td>""" % yn(c['powerOn'])
    print """<td>%s</td>""" % yn(c['targetMet'])
    print "</tr>"

#dict_.get('key2', "Key doesn't exist")

print "</table>"
print "<br>"
checkwatchdog = int(time.time())
watchdog = status['watchDog']
if abs(watchdog - checkwatchdog) > 10:
    print "<h1>Controller Crashed</h1>"
else:
    print "Controller status: ", status['runStop']

print """\
<br><br>
<form method="get" action="ctrlform.py">
<input type="submit" value="Settings">
</form>
"""

print """\
</body>
</html>
"""
