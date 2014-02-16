from bottle import Bottle, ServerAdapter, route, run
from threading import Thread
import time
import urllib2

import stagestatus


def testStagestatus():
    def begin():
        run(server=server)

    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True

    Thread(target=begin).start()
    print "Server started"
    time.sleep(0.1)
    aResp = urllib2.urlopen("http://localhost:8080/stagestatus")
    server.stop()
    print "Server stopped"

    web_pg = aResp.read()
    assert "Brew Stages" in web_pg
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
    testStagestatus()
