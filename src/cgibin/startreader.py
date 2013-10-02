#!/usr/bin/python
import cgi
import cgitb

import dataMemcache


def startreaderMain():
    cgitb.enable()
    myData = dataMemcache.brewData()
    form = cgi.FieldStorage()  # instantiate only once!

    if 'runStatus' in form:
        runStatus = form['runStatus'].value
        if runStatus != 'run':
            runStatus = 'stop'
        myData.setRunStatus(runStatus)

    if 'pauseState' in form:
        pauseState = form['pauseState'].value
        myData.setPause(pauseState == 'True')

    if 'skipState' in form:
        skipState = form['skipState'].value
        myData.setSkip(skipState == 'True')

    if 'errorState' in form:
        errorState = form['errorState'].value
        if errorState == 'False':
            myData.unsetError()

    print "Content-Type: text/html"
    print
    print """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
       "http://www.w3.org/TR/html4/loose.dtd">
       <html>
         <head>
           <title></title>
    <meta HTTP-EQUIV="REFRESH" content="0; url=/index.html">
     </head>
    """
    print """\
    <body><h1>RecipeReader</h1>
    <p>This is the page that should redirect</p>
    <p>The purpose of this page is to read form data and update data files.</p>
    <br><br>
    """

    print "</body></html>"

if __name__ == "__main__":
    startreaderMain()
