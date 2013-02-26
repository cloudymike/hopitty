#!/usr/bin/python
import pickle
import cgi
import cgitb
import time
import memcache
#@PydevCodeAnalysisIgnore
import recipelist
from recipelist import recipeListClass


if __name__ == "__main__":
    myrecipe = recipelist.recipeListClass()
    sys.exit(1)
    """
    This is an example file, reading some useful value in a recipe file
    Mostly for debugging
    """
    cgitb.enable()

    print "Content-Type: text/html"
    print
    print '<META HTTP-EQUIV="REFRESH" CONTENT="1">'
    print """\
    <html>
    <body>
    <h1>Recipe list</h1>
    """

    print """\
    </body>
    </html>
    """
