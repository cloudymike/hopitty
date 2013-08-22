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
    runStatus = myData.getRunStatus()
    pauseState = myData.getPause()
    skipState = myData.getSkip()
    errorState = myData.getError()

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
    print "Start/stop brewing program"
    print '</form>'

    print '<form method="get" action="startreader.py">'
    if pauseState:
        print '<input type="hidden" name="pauseState" value="False">'
        print '<input type="submit"'
        print """
        style="color: white; background-color: green; font-size: larger;
        height:50px;width:80px;"
        """
        print ' value="Resume">'
    else:
        print '<input type="hidden" name="pauseState" value="True">'
        print '<input type="submit"'
        print """
        style="color: black; background-color: yellow; font-size: larger;
        height:50px;width:80px;"
        """
        print ' value="Pause">'
    print "Pause brewing process temporarily"
    print '</form>'

    print '<form method="get" action="startreader.py">'
    if skipState:
        print '<input type="hidden" name="skipState" value="False">'
        print '<input type="submit"'
        print """
        style="color: grey; background-color: white; font-size: larger;
        height:50px;width:80px;"
        """
        print ' value="Skip">'
    else:
        print '<input type="hidden" name="skipState" value="True">'
        print '<input type="submit"'
        print """
        style="color: black; background-color: white; font-size: larger;
        height:50px;width:80px;"
        """
        print ' value="Skip">'
    print "Skip one stage forward."
    print '</form>'

    print '<form method="get" action="startreader.py">'
    if errorState:
        print '<input type="hidden" name="errorState" value="False">'
        print '<input type="submit"'
        print """
        style="color: black; background-color: red; font-size: larger;
        height:50px;width:80px;"
        """
        print ' value="Error">'
    else:
        print '<input type="hidden" name="errorState" value="True">'
        print '<input type="submit"'
        print """
        style="color: black; background-color: white; font-size: larger;
        height:50px;width:80px;"
        """
        print ' value="OK">'

    print "Clear error."
    print '</form>'

    common.footer(__file__)


if __name__ == "__main__":
    startMain()
