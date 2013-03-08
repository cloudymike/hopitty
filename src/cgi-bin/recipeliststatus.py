#!/usr/bin/python
import pickle
import cgi
import cgitb
import time
import sys

import memcache
#@PydevCodeAnalysisIgnore

DEBUG = False


def objectFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    pickledObject = mc.get(key)
    object = pickle.loads(pickledObject)
    return(object)


def getListFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    recipeNameList = mc.get(key)
    return(recipeNameList)


def getCurrentRecipeFromMemcache():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    try:
        stat = mc.get('hopitty_run_key')
        recipe = stat['name']
    except:
        if DEBUG:
            try:
                recipe = mc.get('currentRecipe')
            except:
                recipe = ""
        else:
            recipe = ""
    return(recipe)


# Use this in final production
def getCurrentStatusRecipeFromMemcache():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    try:
        recipe = mc.get('hopitty_run_key')
    except:
        recipe = ""
    return(recipe)


if __name__ == "__main__":
    recipeList = getListFromMemcache('recipeNameList')
    recipeList.sort()

    """
    This is an example file, reading some useful value in a recipe file
    Mostly for debugging
    """
    cgitb.enable()

    print "Content-Type: text/html"
    print
    print """\
    <html>
    <body>
    <h1>Recipe list</h1>
    """

    print "Current Recipe:", getCurrentRecipeFromMemcache()
    print '<form method="get" action="recipereader.py">'
    for recipeName in recipeList:
        rnstr = "\"" + recipeName + "\""
        if recipeName == getCurrentRecipeFromMemcache():
            sel = "checked"
        else:
            sel = ""

        print '<input type="radio" name="recipe" value=', rnstr, sel, ">", \
        recipeName, '<br>'
    print '<input type="submit" value="Set">'

    print '</form>'

    print '<a href="/index.html"><button>Home</button></a>'
    print '<a href="status.py"><button>Status</button></a>'
    print '<a href="stagesstatus.py"><button>Stages</button></a>'
    print '<a href="recipeliststatus.py"><button>Refresh</button></a>'
    print """\
    </body>
    </html>
    """
