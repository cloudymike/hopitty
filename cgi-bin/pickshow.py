#!/usr/bin/python
import pickle
import cgi
import cgitb 

cgitb.enable()

form = cgi.FieldStorage() # instantiate only once!
setTime = form.getfirst('name', 'empty')

# Avoid script injection escaping the user input
setTime = cgi.escape(setTime)

settings = {'time': setTime,
    'name': 'JustMe'
}
output = open('/tmp/settings.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(settings, output)
output.close()


data=pickle.load(open("/tmp/data.pkl","rb"))
myname = data['me']
time=data['t']
status=data['status']
print "Content-Type: text/html"
print
print '<META HTTP-EQUIV="REFRESH" CONTENT="5">'
print """\
<html>
<body>
<h2>Hello %s</h2>
""" % myname
print """<h1>Temp: %s F</h1>""" % time
print """<p>Set Temp: %s F</p>""" % setTime
print """<p>Hot Plate: %s </p>""" % status
print """\
<form method="get" action="n2.py">
<input type="hidden" name="name" value="%s">
<input type="submit" value="Set Temp">
</form>
"""  % setTime
print """\
<a href="n2.py">Set temp</a>
"""
print """\
</body>
</html>
"""
