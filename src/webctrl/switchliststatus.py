import bottle
from bottle import route, run, template, error, get, post
from bottle import request, response, redirect

import commonweb


def switchliststatus(switchDict, selectSwitch, currentSwitch):
    retstr = "<h1>Recipe list</h1>"
    cweb = commonweb.commonweb()
    print switchDict
    if selectSwitch is None:
        selectSwitch = ""

    if currentSwitch is None:
        currentSwitch = ""

    retstr = retstr + "<b>Current running Recipe :</b>" + \
        currentSwitch + "<br><br>\n"
    retstr = retstr + "<b>Current Selected Recipe:</b>" + \
        selectSwitch + "<br><br>\n"
    retstr = retstr + '<form method="post" action="/switchlist">'

    for switchName, switchStatus in switchDict.iteritems():
        rnstr = "\"" + switchName + "\""
        if switchStatus:
            sel = "checked"
            retstr = retstr + "<b>"
        else:
            sel = ""

        retstr = retstr + '<input type="CHECKBOX" name="switch" value='
        retstr = retstr + rnstr + sel + ">" + switchName + '</b></u><br>\n'
        #<input type="submit" class="f" name="next" value="Next">
    retstr = retstr + '<input type="submit" value="Update">'

    retstr = retstr + '</form>'
    retstr = retstr + cweb.footer()
    return(retstr)
