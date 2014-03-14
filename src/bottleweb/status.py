import dataMemcache
import bottle
import commonweb
import time


def yn(status):
    if status:
        return("y")
    else:
        return("n")


@bottle.route('/status')
def status():
    common = commonweb.commonweb()
    myData = dataMemcache.brewData()
    #status = myData.getStatus()
    stage = myData.getCurrentStage()

    errorState = myData.getError()
    # errorState = False
    highLightColor = """<tr style="background-color:green;color:white;">"""
    if errorState:
        highLightColor = """<tr style="background-color:red;color:white;">"""

    # If there is not status, set some default vals to
    # not break but rather show empty values
    #if len(status) == 0:
    #        status = {}
    #        status['controllers'] = {}
            #status['runStop'] = 'Unknown'
            #status['watchDog'] = 0
            #status['stage'] = 'Unknown'
    #        status['name'] = 'Unknown'

    controllers = myData.getControllersStatus()

    retstr = common.header("Brew Status", True)

    retstr = retstr + """<h2>%s</h2>""" % myData.getCurrentRecipe()
    retstr = retstr + """<h3>Stage: %s</h3>""" % stage

    if myData.getCtrlRunning():
        retstr = retstr + """\
        <table border="1">
        <tr>
        <td><b>Controller</b></td>
        <td><b>Active</b></td>
        <td><b>Set Value</b></td>
        <td><b>Actual Value</b></td>
        <td><b>Power</b></td>
        <td><b>Done</b></td>
        </tr>
        """
        for key, c in controllers.items():
            if c['active']:
                retstr = retstr + highLightColor
            else:
                retstr = retstr + """
                    <tr style="background-color:white;color:gray;">
                    """
            retstr = retstr + """<td> %s </td>""" % key
            retstr = retstr + """<td>  %s  </td>""" % yn(c['active'])
            if c['unit'] is None:
                retstr = retstr + """<td> </td>"""
                retstr = retstr + """<td> </td>"""
            else:
                retstr = retstr + """<td> %.2f %s</td>""" %\
                    (c['target'], c['unit'])
                retstr = retstr + """<td> %.2f %s</td>""" %\
                    (c['actual'], c['unit'])
            retstr = retstr + """<td> %s </td>""" % yn(c['powerOn'])
            retstr = retstr + """<td>%s</td>""" % yn(c['targetMet'])
            retstr = retstr + "</tr>"

        retstr = retstr + "</table>"
    retstr = retstr + "<br>"
    #checkwatchdog = int(time.time())
    #watchdog = status['watchDog']
    #if abs(watchdog - checkwatchdog) > 10:
    if myData.checkWatchdog():
        retstr = retstr + "<h1>ERROR: Controller not responding</h1>"
    elif myData.getCtrlRunning and myData.getPause():
        retstr = retstr + "Controller running, but paused"
    elif myData.getCtrlRunning and not myData.getPause():
        retstr = retstr + "Controller running"
    elif not myData.getCtrlRunning:
        retstr = retstr + "Controller running, but paused"
    else:
        retstr = retstr + "Controller state unknown"

#    print """\
#    <form method="get" action="ctrlform.py">
#    <input type="submit" value="Settings">
#    </form>
#    """

    retstr = retstr + common.footer()
    return(retstr)