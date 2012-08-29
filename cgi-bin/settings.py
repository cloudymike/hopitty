#!/usr/bin/python
import cgi
import pickle
import cgitb 

cgitb.enable()

print "Content-Type: text/html"
print
print """\
<html>
<meta HTTP-EQUIV="REFRESH" content="0; url=pickshow.py">
<body><h1>This is red</h1>
<p>This is the page that should redirect</p>
</body>
</html>
"""

#<meta HTTP-EQUIV="REFRESH" content="0; url=pickshow.py">

