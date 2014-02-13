from bottle import Bottle, ServerAdapter, route, run
from threading import Thread
import time
import urllib
import urllib2


class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw):
                    pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler,
                                  **self.options)
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


# A web page, any webpage
@route('/')
def index():
    return("hello world")


def begin():
    run(server=server)


if __name__ == '__main__':
    server = MyWSGIRefServer(host="localhost", port=8080)
    Thread(target=begin).start()
    print "Server started"
    time.sleep(1)
    aResp = urllib2.urlopen("http://localhost:8080")
    web_pg = aResp.read()
    print web_pg
    server.stop()
    print "Server stopped"
    assert "hello world" in web_pg
    print "test passed"
