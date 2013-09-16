#!/usr/bin/python
import cgitb

import commonweb
import dataMemcache


def stageStatusMain():
    common = commonweb.commonweb()
    myData = dataMemcache.brewData()
    stages = myData.getStagesList()
    status = myData.getStatus()
    currentStage = myData.getCurrentStage()

    cgitb.enable()

    errorState = myData.getError()
    highLightColor = """<tr style="background-color:green;color:white;">"""
    if errorState:
        highLightColor = """<tr style="background-color:red;color:white;">"""

    common.header("Brew Stages", True)
    print """<h2>%s</h2>""" % myData.getCurrentRecipe()

    if myData.getRunStatus() == 'run':
        print '<table border="1"><tr>'
        print '<td><b> Stage </b></td>'
        ctrlList = myData.getControllerList()
        for c in ctrlList:
            print "<th>", c, "</th>"
        print '</tr>'
        for stage, step in sorted(stages.items()):
            if stage == currentStage:
                print highLightColor
            else:
                print """<tr style="background-color:white;color:black;">"""
            print "<td>", stage, "</td>"
            for c in ctrlList:
                if step[c]['active']:
                    print "<td>", step[c]['targetValue'], "</td>"
                else:
                    print "<td> </td>"
            print "</tr>"
        print "</table>"

    common.footer(__file__)

if __name__ == "__main__":
    stageStatusMain()
