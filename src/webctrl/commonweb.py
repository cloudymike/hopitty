import sys


class commonweb():
    def __init__(self):
        pass

    def header(self, title, refresh=False):
        retstr = """
       <head>
       <link rel="stylesheet" href="static/style.css">
       <title>%s</title>
        """ % title
        if refresh:
            retstr = retstr + '<META HTTP-EQUIV="REFRESH" CONTENT="10">'
        retstr = retstr + """
       
        </head>
        <body>
        <h1>%s</h1>
        """ % title
        return(retstr)

    def footer(self):
        retstr = "<br><br>"
        retstr = retstr + '<a href="/"><button>Home</button></a>'
        retstr = retstr + '<a href="/start"><button>Run Control</button></a>'
        retstr = retstr + '<a href="/status"><button>Status</button></a>'
        #retstr = retstr + '<a href="/stagestatus"><button>Stages</button></a>'
        retstr = retstr + \
            '<a href="/recipelist"><button>RecipeList</button></a>'
        retstr = retstr + '<a href="/temp"><button>Temp</button></a>'
        retstr = retstr + '<a href="/volume"><button>Volume</button></a>'
        retstr = retstr + \
                 '<a href="/ingredients"><button>Ingredients</button></a>'
        retstr = retstr + '<a href="/gauges"><button>Gauges</button></a>'
        return(retstr)
