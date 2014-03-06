from bottle import Bottle, ServerAdapter, route, run
from threading import Thread
import time
import urllib
import urllib2

import dataMemcache

import start


def testStatus():
    def begin():
        run(server=server)

    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True

    Thread(target=begin).start()
    time.sleep(0.1)
    aResp = urllib2.urlopen("http://localhost:8080/start")
    server.stop()

    web_pg = aResp.read()
    assert 'Run Control' in web_pg
    print "Header test passed"


def testRun():
    def begin():
        run(server=server)

    data = dataMemcache.brewData()
    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True
    data.setCtrlRunning(False)

    Thread(target=begin).start()

    time.sleep(0.1)
    postDataR = urllib.urlencode({"runStatus": "run"})
    aResp = urllib.urlopen("http://localhost:8080/start", postDataR)
    dRun = data.getCtrlRunning()

    postDataS = urllib.urlencode({"runStatus": "stop"})
    aRespF = urllib.urlopen("http://localhost:8080/start", postDataS)

    server.stop()

    assert dRun
    assert not data.getCtrlRunning()

    print "Run test passed"


def testPause():
    def begin():
        run(server=server)

    data = dataMemcache.brewData()
    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True
    data.setCtrlRunning(True)
    data.setPause(False)

    Thread(target=begin).start()

    time.sleep(0.1)
    postData = urllib.urlencode({"pauseState": "True"})
    aResp = urllib.urlopen("http://localhost:8080/start", postData)
    dTrue = data.getPause()

    postDataF = urllib.urlencode({"pauseState": "False"})
    aRespF = urllib.urlopen("http://localhost:8080/start", postDataF)

    server.stop()

    assert dTrue
    assert not data.getPause()
    assert data.getCtrlRunning()

    print "Pause test passed"


def testSkip():
    def begin():
        run(server=server)

    data = dataMemcache.brewData()
    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True
    data.setSkip(False)

    Thread(target=begin).start()

    time.sleep(0.1)
    postData = urllib.urlencode({"skipState": "True"})
    aResp = urllib.urlopen("http://localhost:8080/start", postData)
    dTrue = data.getSkip()

    postDataF = urllib.urlencode({"skipState": "False"})
    aRespF = urllib.urlopen("http://localhost:8080/start", postDataF)
    server.stop()

    assert dTrue
    assert not data.getSkip()

    print "Skip test passed"


def testError():
    def begin():
        run(server=server)

    data = dataMemcache.brewData()
    server = MyWSGIRefServer(host="localhost", port=8080)
    server.quiet = True
    data.unsetError()
    data.setPause(False)
    assert not data.getError()
    assert not data.getPause()

    data.setError()
    assert data.getError()
    assert data.getPause()

    Thread(target=begin).start()

    time.sleep(0.1)

    postDataF = urllib.urlencode({"errorState": "False"})
    aRespF = urllib.urlopen("http://localhost:8080/start", postDataF)
    server.stop()
    assert not data.getError()
    assert not data.getPause()

    print "Error test passed"


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
    testRun()
    testPause()
    testSkip()
    testError()
