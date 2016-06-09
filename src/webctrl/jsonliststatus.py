import bottle
from bottle import route, run, template, error, get, post
from bottle import request, response, redirect

import commonweb
import os

def getJsonDir():
    jsonlist = ['cleanup', 'flushme']

    cp = os.path.dirname(__file__)
    dirname = cp + '/../recipe'
    print dirname
    try:
        dirlist = os.listdir(dirname)
        print "Right first time"
    except:
        try:
            dirname = cp + '/../../recipe'
        except:
            print "Could not find test file"
            print os.getcwd()
            dirname = None

    return(dirname)

def getJsonFiles():
    jsonlist = ['cleanup', 'flushme']
    dirname = getJsonDir()
    if dirname is None:
        return(jsonlist)
    try:
        dirlist = os.listdir(dirname)
    except:
        print "Could not find any files"
        print os.getcwd()
        return(jsonlist)

    return(dirlist)


def jsonliststatus(recipeList, selectedRecipe=None, currentRecipe=None):
    retstr = "<h1>Recipe list</h1>"
    cweb = commonweb.commonweb()
    if recipeList is None:
        recipeList = getJsonFiles() 
    print recipeList
    if selectedRecipe is None:
        selectedRecipe = ""

    if currentRecipe is None:
        currentRecipe = ""

    retstr = retstr + "<b>Current running Recipe :</b>" + \
        currentRecipe + "<br><br>\n"
    retstr = retstr + "<b>Current Selected Recipe:</b>" + \
        selectedRecipe + "<br><br>\n"
    retstr = retstr + '<form method="post" action="/jsonlist">'

    for recipeName in sorted(recipeList):
        rnstr = "\"" + recipeName + "\""
        if recipeName == selectedRecipe:
            sel = "checked"
            retstr = retstr + "<b>"
        else:
            sel = ""

        retstr = retstr + '<input type="radio" name="recipe" value='
        retstr = retstr + rnstr + sel + ">" + recipeName + '</b></u><br>\n'
    retstr = retstr + '<input type="submit" value="Set">'

    retstr = retstr + '</form>'
    retstr = retstr + cweb.footer()
    return(retstr)
