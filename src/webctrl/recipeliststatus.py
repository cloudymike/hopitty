import bottle
from bottle import route, run, template, error, get, post
from bottle import request, response, redirect

import commonweb


def recipeliststatus(recipeList, selectedRecipe, currentRecipe):
    retstr = "<h1>Recipe list</h1>"
    #myData = dataMemcache.brewData()
    cweb = commonweb.commonweb()
    print recipeList
    if selectedRecipe is None:
        selectedRecipe = ""

    if currentRecipe is None:
        currentRecipe = ""

    retstr = retstr + "<b>Current running Recipe :</b>" + \
        currentRecipe + "<br><br>\n"
    retstr = retstr + "<b>Current Selected Recipe:</b>" + \
        selectedRecipe + "<br><br>\n"
    retstr = retstr + '<form method="post" action="/recipelist">'

    for recipeName in recipeList:
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
