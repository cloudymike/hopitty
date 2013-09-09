import sys


class commonweb():
    def __init__(self):
        pass

    def pagelinks(self, caller):
        callList = caller.split('/')
        lastCaller = len(callList) - 1
        retpage = callList[lastCaller]

        print '<a href="/index.html"><button>Home</button></a>'
        print '<a href="start.py"><button>Run Control</button></a>'
        print '<a href="status.py"><button>Status</button></a>'
        print '<a href="stagesstatus.py"><button>Stages</button></a>'
        print '<a href="recipeliststatus.py"><button>RecipeList</button></a>'
        print '<a href="recipe.py"><button>Recipe</button></a>'
        print '<a href=', retpage, '><button>Refresh</button></a>'

    def header(self, title, refresh=False):
        print "Content-Type: text/html"
        print
        if refresh:
            print '<META HTTP-EQUIV="REFRESH" CONTENT="1">'
        print """\
        <html>
        <body>
        <h1>%s</h1>
        """ % title

    def footer(self, caller):
        print "<br>"
        self.pagelinks(caller)
        print """\
        </body>
        </html>
        """
