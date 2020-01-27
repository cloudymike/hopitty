'''
This is a test web server to test the individual pages.
Not all pages are tested as the datastructure needs to be stubbed.
Start with http://localhost:8080 and try the button links!
'''

from bottle import Bottle, ServerAdapter, route, run, template, static_file
#from bottle_rest import json_to_params

#import matplotlib.pyplot as plt, mpld3
#import matplotlib
from threading import Thread
import time
import datetime
import index
import graphPage
import ingredients
import jstest
import gauges
import apitest
import cylinder

# The following lines create a dummy temperature graph for testing
tx = ['11:11:18.719770', '11:11:26.344335', '11:11:38.140248',
      '11:11:47.031451', '11:11:56.059317', '11:12:03.541168',
      '11:12:11.182522', '11:12:18.252898']
ty = [90, 120, 130, 145, 150, 157, 157, 158]
tz = [90, 100, 120, 140, 160, 180, 200, 212]
tm = [150, 149, 148, 149, 150, 151, 150, 150]
te = [72, 73, 72, 71, 70, 71, 72, 72]

class dummyRecipe():
    def ingredientsHops(self):
        return([["dispenser1", "Columbus (Tomahawk)", 1.0000000],["dispenser3", "Centennial", 0.4999252]])

    def ingredientsMisc(self):
        return([["dispenser2", "Whirlflock", 1.0000000]])

def mktj():
    tj = {}
    l = len(tx)
    for i in range(0, len(tx)):
        hwa = {'actual': ty[i]}
        boila = {'actual': tz[i]}
        masha = {'actual': tm[i]}
        enva = {'actual': te[i]}
        status = {'hwt': hwa, 'boiler': boila, 'mash': masha, "env": enva}
        tt = time.strptime(tx[i], "%H:%M:%S.%f")
        dt = datetime.datetime(*tt[:6])

        tj[dt] = status
    return (tj)


class myserver(ServerAdapter):
    """
    An alternative server that can be better controlled with
    threading
    """
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw):    # noqa
                    pass

            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port,
                                  handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

    @route('/')
    def indexPage():            # noqa
        return (index.index())

    @route('/gauges')
    def gauges():                # noqa
        return(gauges.gauges())
        
    # removeme
    @route('/jstest')
    def jstest():                # noqa
        return(jstest.jstest())
    
    @route('/cylinder')
    def mycylinder():                # noqa
        return(cylinder.cylinderAM())
    
    @route('/apipath/currentstage')
    def apicurrentstage():                # noqa
        return(apitest.currentStage())
    
    @route('/apipath/appliance/<appliance>')
    def apiPathWrap(appliance):                # noqa
        return(apitest.apipath(appliance))

    @route('/chart')
    def chart():                # noqa
        return("No such thing")
#        fig = plt.figure()
#        ax = fig.add_subplot(111)
#        bx = fig.add_subplot(111)
#
#        dx = []
#        for t in tx:
#            tt = time.strptime(t, "%H:%M:%S.%f")
#            dt = datetime.datetime(*tt[:6])
#            dx.append(dt)
#
#        print len(dx), dx
#        print len(ty), ty
#        print len(tz), tz
#        dates = matplotlib.dates.date2num(dx)
#        ax.plot_date(dates, ty, 'r-')
#        bx.plot_date(dates, tz, 'b-')
#        return mpld3.fig_to_html(fig)

    @route('/temp')
    def stat():                 # noqa
        return (graphPage.graphPage(mktj(), "hwt", "boiler", "mash", "env"))

    @route('/ingredients')
    def stat():                 # noqa
        recipe=dummyRecipe()
        return (ingredients.ingredients(recipe))

    @route('/static/<filename>')
    def server_static(filename):  # noqa
        return static_file(filename, root='static/')

    @route('/js/<filename>')
    def js(filename):  # noqa
        return static_file(filename, root='js/')

##########################
# Below this line is also in main program

def begin():
    run(server=server)


if __name__ == '__main__':  # pragma: no cover

    print datetime.datetime.now()
    print datetime.datetime.now().time()

    server = myserver(host="0.0.0.0", port=8080)
    server.quiet = False
    print "Starting"
    Thread(target=begin).start()
    time.sleep(60)
    print "Stopping"
    server.stop()
