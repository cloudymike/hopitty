import sys


class commonweb():
    def __init__(self):
        pass

    def header(self, title, refresh=False):
        print "Content-Type: text/html"
        print
        print """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">"""
        print """\
        <html>
        <head>
        <title>%s</title>
        """ % title
        if refresh:
            print '<META HTTP-EQUIV="REFRESH" CONTENT="1">'
        print """\
        </head>
        <body>
        <h1>%s</h1>
        """ % title

    def footer(self):
        retstr = ""
        retstr = retstr + '<a href="/"><button>Home</button></a>'
        retstr = retstr + '<a href="/start"><button>Run Control</button></a>'
        retstr = retstr + '<a href="/status"><button>Status</button></a>'
        retstr = retstr + '<a href="/stages"><button>Stages</button></a>'
        retstr = retstr + \
            '<a href="/recipelist"><button>RecipeList</button></a>'
        retstr = retstr + '<a href="recipe.py"><button>Recipe</button></a>'
        return(retstr)
