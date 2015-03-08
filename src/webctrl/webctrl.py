"""
The main brew loop with integrated bottle and brew2stages.
"""

from bottle import Bottle, request, run
from threading import Thread
import stages2beer
import recipeReader
import time

# Import of the pages views
import commonweb
import statusView
import index
import recipeliststatus
import switchliststatus
import myserver

import recipeModel
import os


class runbrew():
    def __init__(self, controllers, recipelist,
                 server=myserver.myserver(host="0.0.0.0", port=8080)):
        self.count = 0
        self.wapp = Bottle()
        self.controllers = controllers
        self.recipelist = recipelist
        self.server = server
        self.stages = {}
        self.runningRecipeName = ""
        self.selectedRecipeName = ""
        self.recipeObject = None

        self.switchdict = {"lights": True, "camera": False, "sound": True}

        # Routing statements
        self.wapp.route('/status', 'GET', self.statusPage)
        self.wapp.route('/', 'GET', self.indexPage)
        self.wapp.route('/start', 'GET', self.commandPage)
        self.wapp.route('/start', 'POST', self.doCommand)
        self.wapp.route('/recipelist', 'GET', self.recipeliststatusPage)
        self.wapp.route('/recipelist', 'POST', self.dorecipeliststatus)
        self.wapp.route('/debugStages', 'GET', self.debugStages)
        self.wapp.route('/readrecipes', 'GET', self.getTestRecipeList)

        self.wapp.route('/switchlist', 'GET', self.switchliststatusPage)
        self.wapp.route('/switchlist', 'POST', self.doswitchliststatus)

        self.s2b = stages2beer.s2b(controllers, self.stages)

    def getTestRecipeList(self):
        """ Get recipe list in test directory, and return a recipe list"""
        rl = recipeModel.RecipeList()
        #cp = os.getcwd()
        cp = os.path.dirname(__file__)
        filename = cp + '/../tests/Cloud.bsmx'
        print filename
        try:
            rl.readBeerSmith(filename)
            print "Right first time"
        except:
            try:
                rl.readBeerSmith('../tests/Cloud.bsmx')
            except:
                try:
                    rl.readBeerSmith('./tests/Cloud.bsmx')
                except:
                    try:
                        rl.readBeerSmith('src/tests/Cloud.bsmx')
                    except:
                        print "Could not find test file"
                        print os.getcwd()
        self.recipelist = rl

    def startBlocking(self):
        """
        Run in blocking mode. No way to stop this train...
        """
        run(self.wapp, self.server)

    def startNonBlocking(self):
        """
        Run in non-blocking mode as a thread
        """
        Thread(target=self.begin).start()

    def stop(self):
        self.server.stop()
        if self.s2b.isAlive():
            self.s2b.stop()
        del(self.s2b)

    def begin(self):
        run(self.wapp, self.server)

    #@error(404)
    #def error404(self, error):
    #    return 'These are not the droids you are looking for'

    def indexPage(self):
        return(index.index())

    def statusPage(self):
        rs = statusView.statusView(self.s2b,
                                   False,
                                   self.runningRecipeName)
        return(rs)

    def commandPage(self):
        """
        Page to set the run status, i.e. to start the run
        Also prints some useful info about current status
        """
        print "commandPage"
        common = commonweb.commonweb()

        rs = common.header('Run Control')

        rs = rs + "Run status: "
        if self.s2b.isAlive():
            rs = rs + "Alive"
        else:
            rs = rs + "Dead"

        rs = rs + '<br>'
        rs = rs + '<form method="post" action="/start">'

        if self.s2b.stopped():
            rs = rs + '<input type="hidden" name="runStatus" value="run">'
            rs = rs + '<input type="submit"'
            rs = rs + """
            style="color: white; background-color: green; font-size: larger;
            height:50px;width:80px;"
            """
            rs = rs + ' value="Start">'
        else:
            rs = rs + '<input type="hidden" name="runStatus" value="stop">'
            rs = rs + '<input type="submit"'
            rs = rs + """
            style="color: white; background-color: red; font-size: larger;
            height:50px;width:80px;"
            """
            rs = rs + ' value="Stop">'
        rs = rs + "Start/stop brewing program"
        rs = rs + '</form>'

        rs = rs + '<form method="post" action="/start">'
        if self.s2b.paused():
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

        rs = rs + '<input type="hidden" name="skipState" value="True">'
        rs = rs + '<input type="submit"'
        rs = rs + """
        style="color: black; background-color: white; font-size: larger;
        height:50px;width:80px;"
        """
        rs = rs + ' value="Skip">'
        rs = rs + "Skip one stage forward."
        rs = rs + '</form>'

        rs = rs + common.footer()

        return(rs)

    def doCommand(self):
        print "doCommand"
        runStatus = request.forms.get('runStatus')

        if runStatus == 'stop':
            self.s2b.stop()
            self.s2b.unpause()
        elif runStatus == 'run':
            print "starting"
            print self.s2b.isAlive()
            if not self.s2b.isAlive():
                self.runningRecipeName = self.selectedRecipeName
                self.s2b = stages2beer.s2b(self.controllers, self.stages)
                self.s2b.start()

        pauseState = request.forms.get('pauseState')
        if pauseState == "True":
            self.s2b.pause()
        else:
            self.s2b.unpause()

        skipState = request.forms.get('skipState')
        if skipState == "True":
            self.s2b.skip()

        return(self.commandPage())

    def dorecipeliststatus(self):
        self.selectedRecipeName = request.forms.get('recipe')
        self.updateStages()
        return(self.recipeliststatusPage())

    def recipeliststatusPage(self):
        rs = recipeliststatus.recipeliststatus(
            self.recipelist.getNameList(),
            #DEBUG dealing with multithread issue and sqllite
            #self.recipelist.getFixedNameList(),
            self.selectedRecipeName,
            self.runningRecipeName)
        return(rs)

    def updateStages(self):
        """
        A helper function that should be in the recipeClass or recipeListClass
        creates a bsmxStages object
        """
        bsmx = self.recipelist.getRecipe(self.selectedRecipeName).getBSMXdoc()
        self.recipeObject = recipeReader.bsmxStages(bsmx, self.controllers)
        self.stages = self.recipeObject.getStages()

    def debugStages(self):
        common = commonweb.commonweb()
        rs = str(self.stages)
        rs = rs + common.footer()
        return(rs)

    def doswitchliststatus(self):
        print "doswitchliststatus"
        self.selectedSwitchName = request.forms.get('switch')
        print self.selectedSwitchName
        self.switchdict[self.selectedSwitchName] = \
            not self.switchdict[self.selectedSwitchName]
        return(self.switchliststatusPage())

    def switchliststatusPage(self):
        boguslist = ["lights", "camera"]
        ss = switchliststatus.switchliststatus(
            self.switchdict,
            #DEBUG dealing with multithread issue and sqllite
            #self.recipelist.getFixedNameList(),
            "lights",
            "camera")
        return(ss)
