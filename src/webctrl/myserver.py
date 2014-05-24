from bottle import Bottle, ServerAdapter, route, run
from threading import Thread
import time
import urllib2


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


##########################
# Below this line is also in main program

def begin():
    run(server=server)

if __name__ == '__main__':  # pragma: no cover
    server = myserver(host="0.0.0.0", port=8080)
    server.quiet = False
    print "Starting"
    Thread(target=begin).start()
    time.sleep(1)
    print "Stopping"
    server.stop()
