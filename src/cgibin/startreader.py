#!/usr/bin/python
import cgi
import cgitb

import dataMemcache


def startreaderMain():
    cgitb.enable()
    myData = dataMemcache.brewData()
    form = cgi.FieldStorage()  # instantiate only once!
    runStatus = form.getfirst('runStatus', 'empty')

    # Avoid script injection escaping the user input
    runStatus = cgi.escape(runStatus)
    myData.setRunStatus(runStatus)

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
    """ % runStatus

    print "</body></html>"

if __name__ == "__main__":
    startreaderMain()
