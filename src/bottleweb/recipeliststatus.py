import bottle

#import cgitb

#import commonweb
import dataMemcache


@bottle.route('/recipelist')
def recipeliststatusBottle():
    retstr = ""
    myData = dataMemcache.brewData()
    recipeList = myData.getRecipeList()

    #common.header('Recipe list')
    #selectedRecipe = myData.getCurrentRecipe()
    selectedRecipe = myData.getSelectedRecipe()
    if selectedRecipe is None:
        selectedRecipe = ""

    retstr = retstr + "<b>Current Recipe:</b>" + selectedRecipe + "<br><br>"
    retstr = retstr + '<form method="get" action="recipereader.py">'

    for recipeName in recipeList:
        rnstr = "\"" + recipeName + "\""
        if recipeName == selectedRecipe:
            sel = "checked"
        else:
            sel = ""

        retstr = retstr + '<input type="radio" name="recipe" value='
        retstr = retstr + rnstr + sel + ">" + recipeName + '<br>'
    retstr = retstr + '<input type="submit" value="Set">'

    retstr = retstr + '</form>'

    return(retstr)


def dummyF():

    common.footer(__file__)


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
