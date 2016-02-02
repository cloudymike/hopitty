import bottle
import commonweb


def ingredients(recipeObject):
    common = commonweb.commonweb()
    indexpage = """
         <head>
         <title>Hopitty</title>
        </head>
<body>

<h1>Current Ingredients</h1>
"""
    if recipeObject == None:
        hops = """
<h2>Stuff</h2>
<ul>
<li>dispenser 1 </li>
<li>dispenser 2 </li>

</ul>
"""
    else:
        hops = str(recipeObject.ingredientsHops())
    indexpage = indexpage + hops
    indexpage = indexpage + common.footer()
    indexpage = indexpage + "</body>"

    return(indexpage)
