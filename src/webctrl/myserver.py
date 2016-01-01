'''
This is a test web server to test the individual pages.
Not all pages are tested as the datastructure needs to be stubbed.
Start with http://localhost:8080 and try the button links!
'''

from bottle import Bottle, ServerAdapter, route, run, template
import matplotlib.pyplot as plt, mpld3
import matplotlib
from threading import Thread
import time
import datetime
import index
import graphPage

# The following lines create a dummy temperature graph for testing
tx = ['11:11:18.719770', '11:11:26.344335', '11:11:38.140248',
      '11:11:47.031451', '11:11:56.059317', '11:12:03.541168',
      '11:12:11.182522', '11:12:18.252898']
ty = [156, 157, 157, 157, 157, 157, 157, 158]
tz = [160, 159, 158, 157, 156, 155, 154, 153]


def mktj():
    tj = {}
    l = len(tx)
    for i in range(0, len(tx)):
        hwa = {'actual': ty[i]}
        boila = {'actual': tz[i]}
        status = {'hwt': hwa, 'boiler': boila}
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
                def log_request(*args, **kw):
                    pass

            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port,
                                  handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

    @route('/')
    def indexPage():
        return (index.index())

    @route('/chart')
    def chart():
        fig = plt.figure()
        ax = fig.add_subplot(111)
        bx = fig.add_subplot(111)

        dx = []
        for t in tx:
            tt = time.strptime(t, "%H:%M:%S.%f")
            dt = datetime.datetime(*tt[:6])
            dx.append(dt)

        print len(dx), dx
        print len(ty), ty
        print len(tz), tz
        dates = matplotlib.dates.date2num(dx)
        ax.plot_date(dates, ty, 'r-')
        bx.plot_date(dates, tz, 'b-')
        return mpld3.fig_to_html(fig)

    @route('/temp')
    def stat():
        return (graphPage.graphPage(mktj(), "hwt", "boiler"))


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
