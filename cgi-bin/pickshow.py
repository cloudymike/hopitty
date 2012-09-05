#!/usr/bin/python
import pickle
import cgi
import cgitb
import time

cgitb.enable()

data = pickle.load(open("/tmp/data.pkl", "rb"))
myname = data['me']
currentTemp = data['t']
status = data['status']
watchdog = data['watchdog']
checkwatchdog=int(time.time())

settings = pickle.load(open("/tmp/settings.pkl", "rb"))
setTemp = settings['temperature']
setStage = settings['stage']

print "Content-Type: text/html"
print
print '<META HTTP-EQUIV="REFRESH" CONTENT="5">'
print """\
<html>
<body>
<h2>Hi %s</h2>
""" % myname
print """<h1>Temp: %s F</h1>""" % currentTemp
print """<p>Set Temp: %s F</p>""" % setTemp
print """<p>Hot Plate: %s </p>""" % status
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
