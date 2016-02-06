import bottle
import commonweb


def bulletedList(title, list):
    bl = "<b>" + title + "</b><p><ul>"
    for h in list:
        w = "{0:.2f}".format(float(h[2]))
        bl = bl + "<li>" + h[0] + "<ul><li>" + \
             h[1] + " " + w  + "</li></ul></li>"
    bl = bl + "</ul><p>"
    return bl


def ingredients(recipeObject):
    common = commonweb.commonweb()
    indexpage = """
         <head>
         <title>Hopitty</title>
        </head>
<body>

<h1>Current Ingredients</h1>
"""
    if recipeObject is None:
        hops = """
<h2>Stuff</h2>
<ul>
<li>dispenser 1 </li>
<li>dispenser 2 </li>

</ul>
"""
        misc = ""
    else:
        hops = bulletedList('Hops', recipeObject.ingredientsHops())
        misc = bulletedList('Misc', recipeObject.ingredientsMisc())
    indexpage = indexpage + hops + misc
    indexpage = indexpage + common.footer()
    indexpage = indexpage + "</body>"

    return(indexpage)
