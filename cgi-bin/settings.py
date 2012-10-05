#!/usr/bin/python
import cgi
import pickle
import cgitb

cgitb.enable()


form = cgi.FieldStorage()  # instantiate only once!
setTemp = form.getvalue('name', "0")
setTime = form.getvalue('setTime', "0")
setHwVolume = form.getvalue('setHwVolume', "0")
setStage = form.getvalue('stage', 'stop')

# Avoid script injection escaping the user input
setTemp = cgi.escape(setTemp)
setTime = cgi.escape(setTime)
setHwVolume = cgi.escape(setHwVolume)
setStage = cgi.escape(setStage)

settings = {'temperature': setTemp,
    'stage': setStage,
    'name': 'Manual',
    'setTime': setTime,
    'setHwVolume': setHwVolume
}
output = open('/tmp/settings.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(settings, output)
output.close()

print "Content-Type: text/html"
print
print """<html>"""
print """<meta HTTP-EQUIV="REFRESH" content="0; url=status.py">"""
print """\
<body><h1>Settings</h1>
<p>This is the page that should redirect</p>
<p>The purpose of this page is to read form data and update data files.</p>
"""
print """<p>Temp: %s</p>""" % setTemp
print """<p>Time: %s</p>""" % setTime
print """<p>HwVol: %s</p>""" % setHwVolume
print """<p>Stage: %s</p>""" % setStage
print """\
<a href="./status.py">Show Page</a>
</body>
</html>
"""
