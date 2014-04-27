"""
The main brew loop with integrated bottle and brew2stages.
"""

from bottle import Bottle, request
import stages2beer
import recipeReader

# Import of the pages views
import commonweb
import statusView
import index
import recipeliststatus


class runbrew():
    def __init__(self, controllers, recipelist):
        self.count = 0
        self.wapp = Bottle()
        self.controllers = controllers
        self.recipelist = recipelist
        self.stages = {}
        self.runningRecipeName = ""
        self.selectedRecipeName = ""
        self.recipeObject = None

        # Routing statements
        self.wapp.route('/status', 'GET', self.statusPage)
        self.wapp.route('/', 'GET', self.indexPage)
        self.wapp.route('/start', 'GET', self.commandPage)
        self.wapp.route('/start', 'POST', self.doCommand)
        self.wapp.route('/recipelist', 'GET', self.recipeliststatusPage)
        self.wapp.route('/recipelist', 'POST', self.dorecipeliststatus)
        self.wapp.route('/debugStages', 'GET', self.debugStages)

        self.s2b = stages2beer.s2b(controllers, self.stages)

        self.wapp.run(host='localhost', port=8080)

    def __del__(self):
        if self.s2b.isAlive():
            self.s2b.stop()
        del(self.s2b)

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

        rs = rs + common.footer()

        return(rs)

    def doCommand(self):
        print "doCommand"
        runStatus = request.forms.get('runStatus')

        if runStatus == 'stop':
            self.s2b.stop()
        elif runStatus == 'run':
            print "starting"
            print self.s2b.isAlive()
            if not self.s2b.isAlive():
                self.runningRecipeName = self.selectedRecipeName
                self.s2b = stages2beer.s2b(self.controllers, self.stages)
                self.s2b.start()
        return(self.commandPage())

    def dorecipeliststatus(self):
        self.selectedRecipeName = request.forms.get('recipe')
        self.updateStages()
        return(self.recipeliststatusPage())

    def recipeliststatusPage(self):
        rs = recipeliststatus.recipeliststatus(
            self.recipelist.getNameList(),
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
