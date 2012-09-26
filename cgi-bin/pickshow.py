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

data = pickle.load(open("/tmp/data.pkl", "rb"))
myname = data['me']
currentTemp = data['t']
status = data['status']
watchdog = data['watchdog']
currentTime = data['delayTime']
checkwatchdog=int(time.time())

settings = pickle.load(open("/tmp/settings.pkl", "rb"))
setTemp = settings['temperature']
setStage = settings['stage']
setTime = settings['setTime']

print "Content-Type: text/html"
print
print '<META HTTP-EQUIV="REFRESH" CONTENT="5">'
print """\
<html>
<body>
<h2>Hi %s</h2>
""" % myname

print """\
<table border="1">
<tr>
<td><b>Value</td>
<td><b>Set Value</td>
<td><b>Actual Value</td>
<td><b>Done</td>
</tr>
"""
print """<tr><td>Temp</td>"""
print """<td> %s F</td>""" % setTemp
print """<td> %s F</td>""" % currentTemp
print """<td>%s</td>""" % yn(data['hwtDone'])
print "</tr>"

print """<tr><td>Time</td>"""
print """<td> %s min</td>""" % setTime
print """<td> %s min</td>""" % currentTime
print """<td>%s</td>""" % yn(data['delayTimeDone'])
print "</tr>"
print "</table>"

print """<p>Hot Water Tun Heater: %s </p>""" % status
print """<p>Stage: %s </p>""" % setStage
print """\
<form method="get" action="n2.py">
<input type="hidden" name="name" value="%s">
<input type="submit" value="Settings">
</form>
""" % setTemp

if abs(watchdog - checkwatchdog) > 10:
    print "<h1>Controller Crashed</h1>"
print """\
</body>
</html>
"""
