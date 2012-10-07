#!/usr/bin/python
import cgi
import pickle
import cgitb

cgitb.enable()


def TrueY(s):
    if s == 'y':
        return True
    if s == 'Y':
        return True
    return False

form = cgi.FieldStorage()  # instantiate only once!
try:
    status = pickle.load(open("/tmp/status.pkl", "r"))
except:
    status = []
    status['controller'] = []
    status['runStop'] = 'Unknown'
    status['watchDog'] = 0
controllers = status['controllers']

settings = {}
active = {}
for key, c in controllers.items():
    settings[key] = form.getvalue(key, "0")
    activekey = key + "_active"
    active[key] = form.getvalue(activekey, "n")

runStop = form.getvalue('RunStop', 'stop')
#setTemp = form.getvalue('name', "0")

# Avoid script injection escaping the user input
#setTemp = cgi.escape(setTemp)

print "Content-Type: text/html"
print
print """<html>"""
# Uncomment this line to have quick redirect
#print """<meta HTTP-EQUIV="REFRESH" content="0; url=status.py">"""
print """\
<body><h1>Settings</h1>
<p>This is the page that should redirect</p>
<p>The purpose of this page is to read form data and update data files.</p>
"""

print """Run or Stop: %s<br><br>""" % runStop

print """\
<table border="1">
<tr>
<td><b>Controller</td>
<td><b>Set Value</td>
<td><b>Actual Value</td>
<td><b>Active</td>
</tr>
"""

for key, c in controllers.items():
    print """<tr><td> %s </td>""" % key
    print """<td> %s %s</td>""" % (settings[key], c['unit'])
    print """<td> %s %s</td>""" % (c['actual'], c['unit'])
    print """<td> %s </td>""" % active[key]
    print "</tr>"

print "</table>"
print "<br>"

dumpsettings = {}
dumpsettings['runStop'] = runStop

for key, c in controllers.items():
    dumpdict = {}
    dumpdict['targetValue'] = settings[key]
    dumpdict['active'] = TrueY(active[key])
    dumpsettings[key] = dumpdict

output = open('/tmp/settings.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(dumpsettings, output)
output.close()
print "Pickled settings<br>"
print dumpsettings
print "<br>"


print """\
<a href="./status.py">Show Page</a>
</body>
</html>
"""
