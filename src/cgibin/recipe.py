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
    number = 0
    for c in containers:
        number = number + 1
        items = myData.getItemsInContainer(c)
        first = True
        for i in items:
            if number % 2 == 0:
                print """<tr style="background-color:yellow;color:black;">"""
            else:
                print """<tr style="background-color:lightblue;
                         color:black;">"""
            if first:
                print """<td> %s </td>""" % c
            else:
                print """<td>  </td>"""
            first = False
            amount = float(i[1])
            unit = i[3]
            if amount > 16 and unit == 'oz':
                amount = round(amount / 16, 1)
                unit = 'lb'
            print """<td>  %s  </td>""" % i[0]
            print """<td>%s %s</td>""" % (amount, unit)
        print "</tr>"
    print "</table>"
    print "<br>"

    common.footer(__file__)


if __name__ == "__main__":
    md = dataMemcache.brewData()
    recipeMain()
