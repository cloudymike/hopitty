import dataMemcache
import bottle
import commonweb
import time


@bottle.route('/stagestatus')
def stagestatus():
    common = commonweb.commonweb()
    myData = dataMemcache.brewData()
    stages = myData.getStagesList()
    status = myData.getStatus()
    currentStage = myData.getCurrentStage()

    errorState = myData.getError()
    highLightColor = """<tr style="background-color:green;color:white;">"""
    if errorState:
        highLightColor = """<tr style="background-color:red;color:white;">"""

    rs = common.header("Brew Stages", True)
    rs = rs + """<h2>%s</h2>""" % myData.getCurrentRecipe()

    if myData.getRunStatus() == 'run':
        rs = rs + '<table border="1"><tr>'
        rs = rs + '<td><b> Stage </b></td>'
        ctrlList = myData.getControllerList()
        for c in ctrlList:
            rs = rs + "<th>" + str(c) + "</th>"
        rs = rs + '</tr>'
        for stage, step in sorted(stages.items()):
            if stage == currentStage:
                rs = rs + highLightColor
            else:
                rs = rs + """
                    <tr style="background-color:white;color:black;">
                    """
            rs = rs + "<td>" + stage + "</td>"
            for c in ctrlList:
                if step[c]['active']:
                    rs = rs + "<td>" + str(step[c]['targetValue']) + "</td>"
                else:
                    rs = rs + "<td> </td>"
            rs = rs + "</tr>"
        rs = rs + "</table>"

    rs = rs + common.footer()

    return(rs)
