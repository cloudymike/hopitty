#!/usr/bin/python

import cgitb

import commonweb
import dataMemcache


def recipeliststatusMain():
    cgitb.enable()

    common = commonweb.commonweb()

    myData = dataMemcache.brewData()
    recipeList = myData.getRecipeList()

    common.header('Recipe list')
    #selectedRecipe = myData.getCurrentRecipe()
    selectedRecipe = myData.getSelectedRecipe()

    print "<b>Current Recipe:</b>", selectedRecipe, "<br><br>"
    print '<form method="get" action="recipereader.py">'
    for recipeName in recipeList:
        rnstr = "\"" + recipeName + "\""
        if recipeName == selectedRecipe:
            sel = "checked"
        else:
            sel = ""

        print '<input type="radio" name="recipe" value=', rnstr, sel, ">", \
        recipeName, '<br>'
    print '<input type="submit" value="Set">'

    print '</form>'

    common.footer(__file__)

if __name__ == "__main__":
    recipeliststatusMain()
