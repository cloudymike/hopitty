from bottle import Bottle, ServerAdapter, route, run
from threading import Thread
import time
import urllib2
import urllib

import dataMemcache

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


def testHeader():
    def begin():
        run(server=server)

    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True

    Thread(target=begin).start()
    time.sleep(0.1)
    try:
        aResp = urllib2.urlopen("http://localhost:8080/recipelist")
    except:
        print "page read error"
    server.stop()

    web_pg = aResp.read()
    assert "Recipe list" in web_pg
    print "Header test passed"


def testSetRecipe():
    def begin():
        run(server=server)

    bd = dataMemcache.brewData()
    recipelist = ['coolkoelsh', 'maxhop', 'silverdollar']
    bd.setRecipeList(recipelist)
    bd.setCurrentRecipe('coolkoelsh')
    bd.setSelectedRecipe('coolkoelsh')
    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True

    Thread(target=begin).start()
    time.sleep(0.1)
    r1 = urllib2.urlopen("http://localhost:8080/recipelist")
    w1 = r1.read()

    data2 = urllib.urlencode({"recipe": "maxhop"})
    r2 = urllib2.urlopen("http://localhost:8080/recipelist", data2)
    w2 = r2.read()

    server.stop()

    assert "Current Recipe:</b>coolkoelsh" in w1
    assert "Current Recipe:</b>maxhop" in w2

    print "Set recipe test passed"

if __name__ == '__main__':
    testHeader()
    testSetRecipe()
