from bottle import Bottle, ServerAdapter, route, run
from threading import Thread
import time
import urllib2

import webctrl
import helpers


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


@route('/')
def myIndex():
    return(webctrl.index.index())


def testIndex():
    def begin():
        run(server=server)

    p = helpers.findPort()
    print "Using port ", p
    server = MyWSGIRefServer(host="localhost", port=p)

    server.quiet = True

    Thread(target=begin).start()
    print "Server started"
    time.sleep(0.1)
    url = "http://localhost:" + str(p)
    aResp = urllib2.urlopen(url)
    server.stop()
    print "Server stopped"

    web_pg = aResp.read()
    assert "How to brew" in web_pg
    print "test passed"


if __name__ == '__main__':
    testIndex()
