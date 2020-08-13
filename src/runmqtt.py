#!/usr/bin/python

# Run simple loop but with communications



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
import equipment
import os
import communicate
import argparse
import paho.mqtt.client as mqtt


IoT_protocol_name = "x-amzn-mqtt-ca"
aws_iot_endpoint = "a2d09uxsvr5exq-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

HOMEDIR=os.getenv("HOME")
ca = HOMEDIR+"/secrets/certs/awsroot.crt"
cert = HOMEDIR+"/secrets/certs/e27d28a42b-certificate.pem.crt"
private = HOMEDIR+"/secrets/keys/e27d28a42b-private.pem.key"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)
logging.basicConfig(format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO,
        stream=sys.stdout)


def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        logger.error("exception ssl_alpn()")
        raise e


class mqttctrl():
    def __init__(self,
        args,
        controllers=None,
        stages=None):

        self.oldtime = 0
        self.count = 0
        self.state = 'stop'
        self.increment = 1
        self.controllers = controllers

        self.hold_forever = self.controllers.stage_template('holdforever')
        self.hold_forever['holdforever']['delayTimer']['active'] = True
        self.hold_forever['holdforever']['delayTimer']['targetValue'] = 600

        if stages:
            self.stages = stages
        else:
            self.stages = self.hold_forever

        # TODO parameterize the topic and host
        # TODO Break this out and pass do_command as a parameter.
        self.maintopic = 'topic'
        self.client = mqtt.Client("hwctrl")
        logger.info("start connect")

        if args.aws:
            ssl_context= ssl_alpn()
            self.client.tls_set_context(context=ssl_context)
            self.client.connect(aws_iot_endpoint, port=443)
        if args.mqtt:
            self.client.connect("localhost",1883,60)

        # For testing purposes, remove all communication
        # Allows test to run without broker.
        if not args.noqueue:
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.loop_start()
            logger.info("connect success")

        # Create an initial status. No stages, just state is stop
        init_status={}
        init_status['state'] = self.state
        status = json.dumps(init_status)
        #print(status)
        self.set_status(status)

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected with result code "+str(rc))
        client.subscribe("topic/test")

    def on_message(self, client, userdata, msg):
        self.do_command( msg.payload.decode())

    def stop(self):
        self.client.loop_stop()

    def do_command(self, command):
        '''
        This is the command handler, that acts on any message coming in
        '''
        logger.info('Recieved command {}'.format(command))
        if command == 'run':
            self.increment = 1
            self.state = 'run'
        if command == 'pause':
            self.state = 'pause'
        if command == 'terminate':
            self.state = 'terminate'
        if command == 'skip':
            self.state = 'skip'
        if command == 'stop':
            self.state = 'stop'

        if len(command) > 0 and command[0] == '{':
            data = command
            status_string = str(data).replace("'","")
            logger.debug(status_string)
            self.stages = json.loads(status_string)
            self.increment = 0
            self.state = 'stop'

    def set_status(self, message):
        topic = self.maintopic+"/status"
        self.client.publish(topic, message)
        return()

    def run(self):
        """
        Main run loop. Go through each stage of recipe and
        for each stage loop until all targets met.
        no blocking, I.e a separate thread
        """
        logger.info("New run of new recipe")
        for r_key, settings in sorted(self.stages.items()):
            logger.info("New stage: {}".format(r_key))
            self.controllers.stop()
            #print(settings)
            self.controllers.run(settings)
            #self.state='run'
            while not self.controllers.done():
                if self.state == 'pause':
                    self.controllers.pause(settings)
                    print('Pausing...')
                else:
                    self.controllers.run(settings)
                nowtime = time.time()
                deltatime = nowtime - self.oldtime
                self.oldtime = nowtime
                difftime = 1.0 - deltatime
                if abs(difftime) > 10:
                    difftime = 0
                sleeptime = max(1.0 + difftime, 0.0)
                sleeptime = min(1.0, sleeptime)
                time.sleep(sleeptime)
                self.controllers.logstatus()
                lightstatus = self.controllers.lightStatus()
                delayTimer = lightstatus['delayTimer']['actual']
                fullstatus = {}
                fullstatus['stage'] = str(r_key)
                fullstatus['state'] = str(self.state)
                fullstatus['status'] = lightstatus
                status = json.dumps(fullstatus)
                print("{} {} {}".format(self.state, r_key, delayTimer))
                self.set_status(status)


                # If state is terminate, return and finish the program
                # If state is stop, return and let start loop reload
                if self.state in ['terminate', 'stop']:
                    self.controllers.stop()
                    return()
                if self.state in ['skip']:
                    self.state = 'run'
                    break

    def start(self):
        while 1:

            mystatus={}
            mystatus['state'] = self.state
            status = json.dumps(mystatus)
            print("Start loop. State: {}".format(self.state))

            self.set_status(status)
            self.controllers.stop()
            time.sleep(1)

            if self.state in ['run']:
                logger.info('New set of stages')
                self.run()

            # If state is terminate, return and finish the program
            # Do any cleanup required
            if self.state == 'terminate':
                return()

            # Either we are done or the stop signal is sent
            # Eitherway set to stop and add forever loop
            if self.state != 'stop':
                self.state = 'stop'

    def quickRun(self):
        """
        Runs through the recipe without any delay to just check it is OK
        This is different from check recipe in that it will also run
        each controller, thus test hardware if connected and not
        permissive
        """
        self.controllers.stop()
        for r_key, settings in sorted(self.stages.items()):
            logger.info("New stage: {}".format(r_key))
            try:
                self.controllers.run(settings)
                self.controllers.stopCurrent(settings)
            except:
                return(False)
        return(True)


if __name__ == "__main__":
#    simTemp = 70
#    shutdown = False


    logger.info('Starting...')

    parser = argparse.ArgumentParser(description='Run brew equiipment with communication enabled for control.')
    parser.add_argument('-c', '--checkonly', action='store_true', help='Only check, do not brew')
    parser.add_argument('-e', '--equipment', action='store_true', help='Force use of real equipment')
    parser.add_argument('-b', '--bsmx', default=None, help='Beersmith file to use, bsmx format, ')
    parser.add_argument('-f', '--file', default=None, type=str, help='Recipe file to use, json format, ')
    parser.add_argument('-r', '--raw', default=None, type=str, help='Stages file to use, json format, ')
    parser.add_argument('-q', '--quick', action='store_true', help='Run quick recipe with no delays, or meeting goals')
    parser.add_argument('-s', '--simulate', action='store_true', help='Force simulation')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='store_true', help='Print version and exit')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--noqueue", action='store_true', help='Do not use communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')

    args = parser.parse_args()
    permissive = True

    #if args.netsock:
    #    logger.error("Netsock not currently supported")
    #    sys.exit(1)

    if args.aws:
        logger.error("AWS mqtt not currently supported")
        sys.exit(1)

    mypath = os.path.dirname(os.path.realpath(__file__))
    e = equipment.allEquipment(mypath + '/equipment/*.yaml')
    myequipment = e.get('Grain 3G, 5Gcooler, 5Gpot, platechiller')

    if args.equipment:
        args.simulate = False

    controllers = ctrl.setupControllers(args.verbose, args.simulate, permissive, myequipment)
    if args.equipment:
        if controllers.HWOK():
            logger.info('USB devices connected')
        else:
            logger.info('ERROR: Missing USB devices, exiting')
            sys.exit(1)

    # Read one of the recipe files
    if args.file:
        j = recipeReader.jsonStages(args.file, controllers)
        if not j.isValid():
            logger.error("Error: bad json recipe")
            sys.exit(1)
        else:
            stages = j.getStages()
    elif args.bsmx:
        b = recipeReader.bsmxStages(args.bsmx, controllers)
        if not b.isValid():
            logger.error("Error: bad Beersmith recipe")
            sys.exit(1)
        else:
            stages = b.getStages()
    elif args.raw:
        with open(args.raw) as data_file:
            stages = json.load(data_file)
    else:
        stages = {}

    equipmentchecker = checker.equipment(controllers, stages)



    if not equipmentchecker.check():
        logger.error("Error: equipment vs recipe validation failed")

    #devices = deviceloop(controllers, stages)
    mc = mqttctrl(args, controllers, stages)

    if not args.checkonly:
        if (stages != {}) and (stages is not None):
            logger.info("Starting single run-through")
            if args.quick:
                if not mc.quickRun():
                    logger.error("Quickrun failed")
                    sys.exit(1)
            else:
                mc.run()
        else:
            logger.info("Starting run loop")
            mc.start()


    logger.info(" ")
    logger.info("OK")
    logger.info("Shutting down")
    mc.stop()
    del controllers

    sys.exit(0)
