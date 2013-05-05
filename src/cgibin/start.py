#!/usr/bin/python

import cgitb

import commonweb
import dataMemcache


def startMain():
    """
    Page to set the run status, i.e. to start the run
    Also prints some useful info about current status
    """
    cgitb.enable()
    common = commonweb.commonweb()
    myData = dataMemcache.brewData()

    common.header('Run Control')

    print "Current Recipe: ", myData.getCurrentRecipe(), '<br>'
    print "Current Stage: ", myData.getCurrentStage(), '<br>'
    runStatus = myData.getRunStatus()
    print "Run status: ", runStatus, '<br>'
    print '<form method="get" action="startreader.py">'
#    if runStatus != 'run':
#        print '<input type="hidden" name="runStatus" value="run">'
#    print '<input type="submit"'
    if runStatus == 'run':
        print '<input type="hidden" name="runStatus" value="stop">'
        print '<input type="submit"'
        print """
        style="color: white; background-color: red; font-size: larger;
        height:50px;width:80px;"
        """
        print ' value="Stop">'
    else:
        print '<input type="hidden" name="runStatus" value="run">'
        print '<input type="submit"'
        print """
        style="color: white; background-color: green; font-size: larger;
        height:50px;width:80px;"
        """
        print ' value="Start">'

    print '</form>'

    common.footer(__file__)


if __name__ == "__main__":
    startMain()
