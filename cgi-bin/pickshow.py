#!/usr/bin/python
import pickle
import cgi
import cgitb 

cgitb.enable()



data=pickle.load(open("/tmp/data.pkl","rb"))
myname = data['me']
currentTemp=data['t']
status=data['status']

settings=pickle.load(open("/tmp/settings.pkl","rb"))
setTemp=settings['temperature']
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
print """\
<form method="get" action="n2.py">
<input type="hidden" name="name" value="%s">
<input type="submit" value="Set Temp">
</form>
"""  % setTemp
print """\
</body>
</html>
"""
