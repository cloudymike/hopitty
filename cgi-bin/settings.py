#!/usr/bin/python
import cgi
import pickle
import cgitb

cgitb.enable()


form = cgi.FieldStorage()  # instantiate only once!
setTemp = form.getvalue('name', "0")
setStage = form.getvalue('stage', 'stop')

# Avoid script injection escaping the user input
setTemp = cgi.escape(setTemp)
setStage = cgi.escape(setStage)

settings = {'temperature': setTemp,
    'stage': setStage,
    'name': 'JustMe'
}
output = open('/tmp/settings.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(settings, output)
output.close()

print "Content-Type: text/html"
print
print """\
<html>
<meta HTTP-EQUIV="REFRESH" content="0; url=pickshow.py">
<body><h1>Settings</h1>
<p>This is the page that should redirect</p>
<p>The purpose of this page is to read form data and update data files.</p>
</body>
</html>
"""
