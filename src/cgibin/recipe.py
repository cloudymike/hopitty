#!/usr/bin/python
import pickle
import cgi
import cgitb
import time

import commonweb
import dataMemcache


def recipeMain():
    cgitb.enable()

    common = commonweb.commonweb()
    myData = dataMemcache.brewData()

    common.header("Recipe", False)

    print """<h2>%s</h2>""" % myData.getCurrentRecipe()

    print """\
    <table border="1">
    <tr>
    <td><b>Container</td>
    <td><b>Item</td>
    <td><b>Amount</td>
    </tr>
    """

    containers = myData.getRecipeContainers()
    for c in containers:
        items = myData.getItemsInContainer(c)
        first = True
        for i in items:
            print """<tr style="background-color:white;color:black;">"""
            if first:
                print """<td> %s </td>""" % c
            else:
                print """<td>  </td>"""
            first = False
            print """<td>  %s  </td>""" % i[0]
            print """<td>%s oz</td>""" % i[1]
        print "</tr>"
    print "</table>"
    print "<br>"

    common.footer(__file__)


if __name__ == "__main__":
    md = dataMemcache.brewData()
    recipeMain()
