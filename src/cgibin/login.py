#!/usr/bin/python

import cgitb

import commonweb
import dataMemcache


def startLogin():
    """
    Page to set the run status, i.e. to start the run
    Also prints some useful info about current status
    """
    cgitb.enable()
    common = commonweb.commonweb()
    myData = dataMemcache.brewData()

    common.header('Run Control')
    runStatus = myData.getRunStatus()
    pauseState = myData.getPause()
    skipState = myData.getSkip()

    print "Current Recipe: ", myData.getCurrentRecipe(), '<br>'
    print "Current Stage: ", myData.getCurrentStage(), '<br>'

    print "Run status: "
    if runStatus != 'run':
        print "Stopped"
    else:
        if pauseState:
            print "Paused"
        else:
            print "Running"

    print '<br>'

    print '<form id="login" action="http://beersmithrecipes.com/myrecipes"'
    print 'method="post" accept-charset="UTF-8">'
    print '<input type="hidden" name="submitted" id="submitted" value="1"/>'
    print '<input type="hidden" name="action" id="action" value="dologin"/>'
    print '<label for="username" >User Name:</label>'
    print '<input type="text" name="uname" id="uname"  maxlength="50" />'
    print '<br>'
    print '<label for="password" >Password:</label>'
    print '<input type="password" name="password"'
    print 'id="password" maxlength="50" />'
    print '</br>'
    print '<center><input type="submit" name="Submit" value="Login" /><center>'
    print '</form>'

    common.footer(__file__)


if __name__ == "__main__":
    startLogin()
