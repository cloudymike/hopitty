import bottle
from bottle import route, run, template, error, get, post
from bottle import request, response, redirect

import commonweb
import dataMemcache


@get('/start')
def start():
    """
    Page to set the run status, i.e. to start the run
    Also prints some useful info about current status
    """
    common = commonweb.commonweb()
    myData = dataMemcache.brewData()

    rs = common.header('Run Control')
    runStatus = myData.getRunStatus()
    pauseState = myData.getPause()
    skipState = myData.getSkip()
    errorState = myData.getError()

    rs = rs + "Current Recipe: " + str(myData.getCurrentRecipe()) + '<br>'
    rs = rs + "Current Stage: " + str(myData.getCurrentStage()) + '<br>'

    rs = rs + "Run status: "
    if runStatus != 'run':
        rs = rs + "Stopped"
    else:
        if pauseState:
            rs = rs + "Paused"
        else:
            rs = rs + "Running"

    rs = rs + '<br>'
    rs = rs + '<form method="post" action="/start">'
#    if runStatus != 'run':
#        print '<input type="hidden" name="runStatus" value="run">'
#    print '<input type="submit"'
    if runStatus == 'run':
        rs = rs + '<input type="hidden" name="runStatus" value="stop">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: white; background-color: red; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="Stop">'
    else:
        rs = rs + '<input type="hidden" name="runStatus" value="run">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: white; background-color: green; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="Start">'
    rs = rs + "Start/stop brewing program"
    rs = rs + '</form>'

    rs = rs + '<form method="post" action="/start">'
    if pauseState:
        rs = rs + '<input type="hidden" name="pauseState" value="False">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: white; background-color: green; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="Resume">'
    else:
        rs = rs + '<input type="hidden" name="pauseState" value="True">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: black; background-color: yellow; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="Pause">'
    rs = rs + "Pause brewing process temporarily"
    rs = rs + '</form>'

    rs = rs + '<form method="post" action="/start">'
    if skipState:
        rs = rs + '<input type="hidden" name="skipState" value="False">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: grey; background-color: white; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="Skip">'
    else:
        rs = rs + '<input type="hidden" name="skipState" value="True">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: black; background-color: white; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="Skip">'
    rs = rs + "Skip one stage forward."
    rs = rs + '</form>'

    rs = rs + '<form method="post" action="/start">'
    if errorState:
        rs = rs + '<input type="hidden" name="errorState" value="False">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: black; background-color: red; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="Error">'
    else:
        rs = rs + '<input type="hidden" name="errorState" value="True">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: black; background-color: white; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="OK">'

    rs = rs + "Clear error."
    rs = rs + '</form>'

    rs = rs + common.footer()

    return(rs)


@post('/start')
def dostart():
    myData = dataMemcache.brewData()

    runStatus = request.forms.get('runStatus')
    if runStatus is not None:
        myData.setRunStatus(runStatus)

    pauseState = request.forms.get('pauseState')
    myData.setPause(pauseState == 'True')

    skipState = request.forms.get('skipState')
    myData.setSkip(skipState == 'True')

    errorState = request.forms.get('errorState')
    if errorState == 'False':
        myData.unsetError()

    return(start())
