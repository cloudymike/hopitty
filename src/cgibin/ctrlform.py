#!/usr/bin/python
import cgi
import pickle
import cgitb

cgitb.enable()
form = cgi.FieldStorage()  # instantiate only once!

try:
    status = pickle.load(open("/tmp/status.pkl", "r"))
except:
    status = []
    status['controller'] = []
    status['runStop'] = 'Unknown'
    status['watchDog'] = 0
controllers = status['controllers']

setRunStop = status['runStop']

print "Content-Type: text/html"
print
print """\
<html>
<h1>Manual setting</h1>
<body>
<form method="get" action="ctrlset.py">
"""
for key, c in controllers.items():
    print """\
%s (%s): <input type="text" name="%s" value="%s">
<input type="checkbox" name="%s_active" value="y">
<br>
""" % (key, c['unit'], key, c['target'], key)


stopchk = ""
runchk = ""
if setRunStop == 'stop':
    stopchk = 'checked="checked"'
if setRunStop == 'run':
    runchk = 'checked="checked"'

print """\
<br><br>
<input type="radio" %s name="RunStop" value="stop" /> Stop<br />
<input type="radio" %s name="RunStop" value="run" /> Run
<br><br>
<input type="submit" value="Set">
</form>""" % (stopchk, runchk)

print "</body></html>"
