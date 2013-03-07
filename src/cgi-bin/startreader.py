#!/usr/bin/python
import cgi
import pickle
import cgitb
import memcache
#@PydevCodeAnalysisIgnore


# This is for debug, set the selected recipe
# directly in mem cache

# This is data that should be sent to controller
def writeRunStatus2Memcache(value):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.set('runStatus', value)

if __name__ == "__main__":
    cgitb.enable()
    form = cgi.FieldStorage()  # instantiate only once!
    runStatus = form.getfirst('runStatus', 'empty')

    # Avoid script injection escaping the user input
    runStatus = cgi.escape(runStatus)
    writeRunStatus2Memcache(runStatus)
    
    print "Content-Type: text/html"
    print
    print '<html>'
    print '<meta HTTP-EQUIV="REFRESH" content="0; url=/index.html">'
    print """\
    <body><h1>RecipeReader</h1>
    <p>This is the page that should redirect</p>
    <p>The purpose of this page is to read form data and update data files.</p>
    <br><br>
    <p>Run status: %s</p>
    """% runStatus

    print "</body></html>"
