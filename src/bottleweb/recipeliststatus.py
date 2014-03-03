import bottle
from bottle import route, run, template, error, get, post
from bottle import request, response, redirect

#import cgitb

import commonweb
import dataMemcache


@get('/recipelist')
def recipeliststatusBottle():
    retstr = "<h1>Recipe list</h1>"
    myData = dataMemcache.brewData()
    cweb = commonweb.commonweb()
    recipeList = myData.getRecipeList()
    selectedRecipe = myData.getSelectedRecipe()
    currentRecipe = myData.getCurrentRecipe()

    if selectedRecipe is None:
        selectedRecipe = ""

    if currentRecipe is None:
        currentRecipe = ""

    retstr = retstr + "<b>Current running Recipe :</b>" + \
        selectedRecipe + "<br><br>\n"
    retstr = retstr + "<b>Current Selected Recipe:</b>" + \
        selectedRecipe + "<br><br>\n"
    retstr = retstr + '<form method="post" action="/recipelist">'

    for recipeName in recipeList:
        rnstr = "\"" + recipeName + "\""
#        if recipeName == currentRecipe:
#            retstr = retstr + "<u>"
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


@post('/recipelist')
def dorecipeliststatusBottle():
    setRecipe = request.forms.get('recipe')
    myData = dataMemcache.brewData()
    #if not myData.getCtrlRunning():
    #    myData.setCurrentRecipe(setRecipe)

    myData.setSelectedRecipe(setRecipe)
    return(recipeliststatusBottle())
