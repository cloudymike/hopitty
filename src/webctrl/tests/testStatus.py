from bottle import Bottle, ServerAdapter, route, run
from threading import Thread
import time
import urllib2
import stages2beer
import ctrl
import appliances

from webctrl import statusView


def timerDict():
    td = {
        "1 stage": {
            "timer": {
                "active": True,
                "targetValue": 1
            }
        }
    }
    return td


def timerCtrl():
    """Instantiate a list of several controllers"""
    ctrl1 = ctrl.controllerList()
    ctrl1.addController('timer', appliances.hoptimer())
    return(ctrl1)


@route('/status')
def statusPage():
    s2b = stages2beer.s2b(timerCtrl(), timerDict())
    s2b.start()
    rs = statusView.statusView(s2b,
                               False,
                               "test recipe")
    s2b.stop()
    return(rs)


def testStatus():
    def begin():
        run(server=server)

    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True

    Thread(target=begin).start()
    print "Server started"
    time.sleep(0.1)
    aResp = urllib2.urlopen("http://localhost:8080/status")
    server.stop()
    print "Server stopped"

    web_pg = aResp.read()
    assert "Brew Status" in web_pg
    print "test passed"


class MyWSGIRefServer(ServerAdapter):
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


if __name__ == '__main__':
    testStatus()
