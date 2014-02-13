from bottle import Bottle, ServerAdapter, route, run
from threading import Thread
import time
import urllib2

import recipeliststatus


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


def testIndex():
    def begin():
        run(server=server)

    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True

    Thread(target=begin).start()
    print "Server started"
    time.sleep(0.1)
    try:
        aResp = urllib2.urlopen("http://localhost:8080/recipelist")
    except:
        print "page read error"
    server.stop()
    print "Server stopped"

    web_pg = aResp.read()
    print web_pg
    assert "Recipe list" in web_pg
    print "test passed"

if __name__ == '__main__':
    testIndex()
