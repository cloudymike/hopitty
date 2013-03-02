#!/usr/bin/python
import pickle
import cgi
import cgitb
import time
import sys


import memcache
#@PydevCodeAnalysisIgnore

def objectFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    pickledObject = mc.get(key)
    object = pickle.loads(pickledObject)
    return(object)

def getListFromMemcache(key):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    recipeNameList = mc.get(key)
    return(recipeNameList)

if __name__ == "__main__":
    recipeList = getListFromMemcache('recipeNameList')
    
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
    for recipeName in recipeList:
        print "<li>",recipeName,"</li>"
   
    print "Yohoo!"
    print """\
    </body>
    </html>
    """
