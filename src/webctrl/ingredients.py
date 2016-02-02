import bottle
import commonweb


def ingredients():
    common = commonweb.commonweb()
    indexpage = """
         <head>
         <title>Hopitty</title>
        </head>
<body>

<h1>Current Ingredients</h1>

<h2>Stuff</h2>
<ul>
<li>dispenser 1 </li>
<li>dispenser 2 </li>

</ul>
"""
    indexpage = indexpage + common.footer()
    indexpage = indexpage + "</body>"

    return(indexpage)
