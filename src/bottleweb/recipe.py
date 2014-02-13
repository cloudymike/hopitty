import bottle
import commonweb
import dataMemcache


@bottle.route('/recipe')
def recipe():
    common = commonweb.commonweb()
    myData = dataMemcache.brewData()

    rs = common.header("Recipe", False)

    rs = rs + """<h2>%s</h2>""" % myData.getCurrentRecipe()

    rs = rs + """\
    <table border="1">
    <tr>
    <td><b>Container</b></td>
    <td><b>Item</b></td>
    <td><b>Amount</b></td>
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
                rs = rs + \
                    """<tr style="background-color:yellow;color:black;">"""
            else:
                rs = rs + """<tr style="background-color:lightblue;
                         color:black;">"""
            if first:
                rs = rs + """<td> %s </td>""" % c
            else:
                rs = rs + """<td>  </td>"""
            first = False
            amount = float(i[1])
            unit = i[3]
            if amount > 16 and unit == 'oz':
                amount = round(amount / 16, 1)
                unit = 'lb'
            rs = rs + """<td>  %s  </td>""" % i[0]
            rs = rs + """<td>%s %s</td>""" % (amount, unit)
        rs = rs + "</tr>"
    rs = rs + "</table>"
    rs = rs + "<br>"

    rs = rs + common.footer()
    return(rs)
