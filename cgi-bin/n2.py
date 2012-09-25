#!/usr/bin/python
import cgi
import pickle
import cgitb

cgitb.enable()
form = cgi.FieldStorage()  # instantiate only once!
setTemp = form.getfirst('name', 'empty')

# Avoid script injection escaping the user input
setTemp = cgi.escape(setTemp)

settings = pickle.load(open("/tmp/settings.pkl", "rb"))
setTemp = settings['temperature']
setStage = settings['stage']
setTime = settings['setTime']

print "Content-Type: text/html"
print
print """\
<html><body>
<form method="get" action="settings.py">
Temperature: <input type="text" name="name" value="%s">

""" % setTemp


print """\
<br>
Delay Time    : <input type="text" name="setTime" value="%s">
<br>
""" % setTime

stopchk = ""
runchk = ""
if setStage == 'stop':
    stopchk = 'checked="checked"'
if setStage == 'run':
    runchk = 'checked="checked"'

print """\
<br><br>
<input type="radio" %s name="stage" value="stop" /> Stop<br />
<input type="radio" %s name="stage" value="run" /> Run
<br><br>
<input type="submit" value="Set">
</form>""" % (stopchk, runchk)

print "</body></html>"
