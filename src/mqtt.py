#!/usr/bin/python

# branch t1
import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

import getopt
import ctrl
import recipeReader
import stages2beer
import checker
import logging
import threading
import time
import json
import fcntl
import os
import paho.mqtt.client as mqtt



def usage():
    print 'usage:'
    print "-h: help"
    print "-c: checkonly"
    print "-f file: read JSON file"
    print "-q: quick check"
    print "-e: Equipment check"
    print "-v: verbose"
    sys.exit

def end_now(logging):
    logging.info(" ")
    logging.info("OK")
    logging.info("Shutting down")
    sys.exit(0)

def oldmain():    
#    simTemp = 70
#    shutdown = False

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.warning('warning test')
    logging.info('Starting...')

    options, remainder = getopt.getopt(sys.argv[1:], 'cef:hqpuv', [
        'checkonly',
        'equipment',
        'file=',
        'help',
        'printRecipe',
        'quick',
        'verbose',
        'version=',
        ])
    verbose = False
    simulation = False
    permissive = True
    quick = False
    checkonly = False
    printRecipe = False
    HWcheck = False
    recipeFile = ""
    bsmxFile = ""
    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-f', '--file'):
            recipeFile = arg
        elif opt in ('-q', '--quick'):
            quick = True
        elif opt in ('-c', '--checkonly'):
            checkonly = True
        elif opt in ('-p', '--printRecipe'):
            printRecipe = True
        elif opt in ('-e', '--equipment'):
            HWcheck = True
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt == '--version':
            version = arg

    # If hardware requirement is set, 
    # check that hardware is connected
    if HWcheck:
        simulation = (simulation or (not HWcheck))
    else:
        simulation = True
    print "Simulation: ", simulation
    controllers = ctrl.setupControllers(verbose, simulation, permissive)
    if HWcheck:
        if controllers.HWOK():
            logging.info('USB devices connected')
        else:
            logging.info('ERROR: Missing USB devices, exiting')
            sys.exit(1)
    loopActive = True
    
    fd = sys.stdin.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    nonblocking = fl | os.O_NONBLOCK
    blocking = fl

    while loopActive:

        # Read one of the recipe files
        if recipeFile == "":
            fcntl.fcntl(fd, fcntl.F_SETFL, blocking)
            print "Try ../jsonStages/base.golden"
            recipeFile = raw_input("Enter your filename: ")
            #recipeFile = sys.stdin.readline().rstrip()
            print "Reading file:",recipeFile
        try:
            with open(recipeFile) as data_file:    
                stages = json.load(data_file)
        except:
            stages = None
        recipeFile = ""

        if stages is None:
            print "Bad recipe file"
        else:
            equipmentchecker = checker.equipment(controllers, stages)
            if not equipmentchecker.check():
                logging.error("Error: equipment vs recipe validation failed")
                stages = None
        
            if (stages == {}) or (stages is None):
                stages = None
                
            brun = stages2beer.s2b(controllers, stages)
            brun.start()
        
            print "-------------------Running-------------------------------"
            
        
            fcntl.fcntl(fd, fcntl.F_SETFL, nonblocking)
            while not brun.stopped() and stages is not None:
                time.sleep(1)
                if brun.paused():
                    print "pause ",
                else:
                    print "run   ",
                print brun.getStage(), " ",
                sdict = brun.getStatus()
                for key, val in sdict.iteritems():
                    print val['actual'],
                print " "
                try:  input = sys.stdin.readline()
                except: continue
                print "INPUT:",input, ":"
                if input[0] == "s":
                    brun.stop()
                    print "\n-----------------Call for stop ------------------------------------"
                if input[0] == "p":
                    brun.pause()
                    print "\n-----------------Call for pause ------------------------------------"
                if input[0] == "c":
                    brun.unpause()
                    print "\n-----------------Call for continue ------------------------------------"
                if input[0] == "n":
                    brun.skip()
                    print "\n-----------------Call for next ------------------------------------"
                    
                
            print "\n-----------------Stopping------------------------------------"
            
            brun.join()

        time.sleep(1)
    
    del controllers
    sys.exit(0)

server = "iot.eclipse.org"
port = 1883
timeout = 60
globalmessage = None

class myval():
    def __init__(self):
        self.value = None
    def set(self,value):
        self.value = value
    def get(self):
        return(self.value)
        
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mhtest2")


def setMessage(message):
    print "Setting",message
    globalmessage=message

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = str(msg.payload)
    sendMessage(client,message)
    setMessage(message)
    print "***"+message+"***"
    print "userdata:",userdata.get()
    userdata.set(message)



def sendMessage(mqttc, message):
    mqttc.publish("mhtest1", message)
    #mqttc.loop(2) 

if __name__ == "__main__":
    me = myval()
    mqttc = mqtt.Client(userdata=me)
    mqttc.connect("test.mosquitto.org", 1883)
    sendMessage(mqttc, "Mo message")
    print "message sent"
    
    mqttc.subscribe("mhtest2")
    #mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.loop_start()
    print "Starting loop"
    run = True
    while run:
        time.sleep(1)
        sys.stdout.write('.')
        sys.stdout.flush()
        if me.get() is not None:
            print "\n",me.get()
            sendMessage(mqttc,me.get())
            if me.get() == "stop":
                run =False
            me.set(None)
        

    
    mqttc.disconnect()
    mqttc.loop_stop()
    sys.exit(0)
