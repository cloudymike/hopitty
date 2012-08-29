#!/usr/bin/python
import cgi
import pickle
import cgitb 

cgitb.enable()
form = cgi.FieldStorage() # instantiate only once!
setTemp = form.getfirst('name', 'empty')

# Avoid script injection escaping the user input
setTemp = cgi.escape(setTemp)

print "Content-Type: text/html"
print
print """\
<html><body>
<form method="get" action="settings.py">
Time: <input type="text" name="name" value="%s">
<input type="submit" value="Set">
</form>
</body></html>
""" % setTemp
