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

    print "<b>Current Recipe:</b>", myData.getCurrentRecipe(), "<br><br>"
    print '<form method="get" action="recipereader.py">'
    for recipeName in recipeList:
        rnstr = "\"" + recipeName + "\""
        if recipeName == myData.getCurrentRecipe():
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
