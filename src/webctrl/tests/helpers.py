from bottle import Bottle, ServerAdapter, route, run
import socket

import ctrl
import appliances
import recipelistmgr
import os
import xml.dom.minidom


def findPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for p in range(8080, 8099):
        print "try port ", p
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', p))
            break
        except socket.error, e:
            print p, "already in use, try", p+1
    return(p)


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


def simpleBsmx():
    retval = """
<Cloud>
 <Name>Cloud</Name>
 <Data>
  <Cloud>
   <F_R_NAME>18 Rune Stone  IPA 2.5G</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Cloud>
  <Cloud>
   <F_R_NAME>19 Great Brew</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Cloud>
 </Data>
</Cloud>
    """
    return(retval)


def getSimpleBSMX():
    """ Get recipe from simpleBSMX, and return a recipe list"""
    rl = recipelistmgr.recipeListClass()
    doc = xml.dom.minidom.parseString(simpleBsmx())
    rl.readBMXdoc(doc)
    rl.printNameList()
    return(rl)


def getTestRecipeList():
    """ Get recipe list in test directory, and return a recipe list"""
    rl = recipelistmgr.recipeListClass()
    #cp = os.getcwd()
    cp = os.path.dirname(__file__)
    filename = cp + '/../../tests/Cloud.bsmx'
    print filename
    try:
        rl.readBeerSmith(filename)
        print "Right first time"
    except:
        try:
            rl.readBeerSmith('../tests/Cloud.bsmx')
        except:
            try:
                rl.readBeerSmith('./tests/Cloud.bsmx')
            except:
                try:
                    rl.readBeerSmith('src/tests/Cloud.bsmx')
                except:
                    print "Could not find test file"
                    print os.getcwd()
    return(rl)
