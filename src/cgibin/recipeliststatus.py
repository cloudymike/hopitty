#!/usr/bin/python
import pickle
import cgi
import cgitb
import time
import sys
import commonweb

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
    try:
        recipeNameList = mc.get(key)
    except:
        recipeNameList = []
    if recipeNameList == None:
        recipeNameList = []
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


def recipeliststatusMain():
    recipeList = getListFromMemcache('recipeNameList')
    recipeList.sort()
    common = commonweb.commonweb()

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

    print "<b>Current Recipe:</b>", getCurrentRecipeFromMemcache(), "<br><br>"
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

    print "<br>"
    common.pagelinks(__file__)
    print """\
    </body>
    </html>
    """


if __name__ == "__main__":
    recipeliststatusMain()
