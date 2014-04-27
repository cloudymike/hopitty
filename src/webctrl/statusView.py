import commonweb


def yn(status):
    if status:
        return("y")
    else:
        return("n")


def statusView(s2b, errorState, currentRecipeName):
    common = commonweb.commonweb()

    #status = s2b.getStatus()
    stage = s2b.getStage()
    ctrlStatus = s2b.getStatus()

    highLightColor = """<tr style="background-color:green;color:white;">"""
    if errorState:
        highLightColor = """<tr style="background-color:red;color:white;">"""

    retstr = common.header("Brew Status", True)

    retstr = retstr + """<h2>Recipe: %s</h2>""" % currentRecipeName
    retstr = retstr + """<h3>Stage: %s</h3>""" % stage

    if s2b.isAlive():
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
        for key, c in ctrlStatus.items():
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

    if not s2b.isAlive():
        retstr = retstr + "<h1>ERROR: Controller not responding</h1>"
    elif s2b.isAlive() and s2b.paused():
        retstr = retstr + "Controller running, but paused"
    elif s2b.isAlive() and not s2b.paused():
        retstr = retstr + "Controller running"
    else:
        retstr = retstr + "Controller state unknown"

    retstr = retstr + common.footer()
    return(retstr)
