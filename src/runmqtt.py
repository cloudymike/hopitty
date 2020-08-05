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
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)


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


class mockctrl():
    def __init__(self,
        args,
        controllers=None,
        stages=None):

        self.oldtime = 0
        self.count = 0
        self.state = 'stop'
        self.increment = 0

        self.hold_forever = controllers.stage_template('holdforever')
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

        logger.info("connect success")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code "+str(rc))
        client.subscribe("topic/test")

    def on_message(self, client, userdata, msg):
        self.do_command( msg.payload.decode())

    def stop(self):
        self.client.loop_stop()

    def do_command(self, command):
        '''
        This is the command handler, that acts on any message coming in
        '''
        if command == 'run':
            self.increment = 1
            self.state = 'run'
        if command == 'pause':
            self.state = 'pause'
            self.increment = 0
        if command == 'terminate':
            self.state = 'terminate'
        if command == 'skip':
            self.state = 'skip'
        if command == 'stop':
            self.increment = 0
            self.state = 'stop'
            self.stages = self.hold_forever

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
        logging.info("New run of new recipe")
        for r_key, settings in sorted(self.stages.items()):
            logging.info("New stage: {}".format(r_key))
            controllers.stop()
            controllers.run(settings)
            self.state='run'
            while not controllers.done() or self.state == 'pause' :
                controllers.run(settings)
                nowtime = time.time()
                deltatime = nowtime - self.oldtime
                self.oldtime = nowtime
                difftime = 1.0 - deltatime
                if abs(difftime) > 10:
                    difftime = 0
                sleeptime = max(1.0 + difftime, 0.0)
                sleeptime = min(1.0, sleeptime)
                time.sleep(sleeptime)
                controllers.logstatus()
                lightstatus = controllers.lightStatus()
                fullstatus = {}
                fullstatus['stage'] = str(r_key)
                fullstatus['state'] = str(self.state)
                fullstatus['status'] = lightstatus
                status = json.dumps(fullstatus)
                #print(status)
                self.set_status(status)


                # If state is terminate, return and finish the program
                # If state is stop, return and let start loop reload
                if self.state in ['terminate','stop']:
                    return()
                if self.state in ['skip']:
                    break


    def start(self):
        while 1:
            logging.info('New set of stages')
            self.run()

            # If state is terminate, return and finish the program
            # Do any cleanup required
            if self.state == 'terminate':
                return()

            # Either we are done or the stop signal is sent
            # Eitherway set to stop and add forever loop
            if self.state != 'stop':
                self.state = 'stop'
                self.stages = self.hold_forever


if __name__ == "__main__":
#    simTemp = 70
#    shutdown = False

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.warning('warning test')
    logging.info('Starting...')

    parser = argparse.ArgumentParser(description='Run brew equiipment with communication enabled for control.')
    parser.add_argument('-b', '--bsmx', default=None, help='Beersmith file to use, bsmx format, ')
    parser.add_argument('-c', '--checkonly', action='store_true', help='Only check, do not brew')
    parser.add_argument('-e', '--equipment', action='store_true', help='Force use of real equipment')
    parser.add_argument('-f', '--file', default="", type=str, help='Stages file to use, json format, ')
    parser.add_argument('-q', '--quick', action='store_true', help='Run quick recipe with no delays, or meeting goals')
    parser.add_argument('-s', '--simulate', action='store_true', help='Force simulation')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='store_true', help='Print version and exit')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')

    args = parser.parse_args()
    permissive = True

    if args.netsock:
        logger.error("Netsock not currently supported")
        sys.exit(1)

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
            logging.info('USB devices connected')
        else:
            logging.info('ERROR: Missing USB devices, exiting')
            sys.exit(1)

    # Read one of the recipe files
    if args.file != "":
        j = recipeReader.jsonStages(args.file, controllers)
        if not j.isValid():
            logging.error("Error: bad json recipe")
        else:
            recipeName = j.getRecipeName()
            stages = j.getStages()
    elif args.bsmx != "" :
        b = recipeReader.bsmxStages(args.bsmx, controllers)
        if not b.isValid():
            logging.error("Error: bad bsmx recipe")
            sys.exit(1)
        else:
            recipeName = b.getRecipeName()
            stages = b.getStages()
    else:
        stages = {}

    #print(stages)

    equipmentchecker = checker.equipment(controllers, stages)



    if not equipmentchecker.check():
        logging.error("Error: equipment vs recipe validation failed")

    #devices = deviceloop(controllers, stages)
    mc = mockctrl(args, controllers, stages)

    if not args.checkonly:
        if (stages != {}) and (stages is not None):
            logging.info("Starting single run-through")
            mc.run()
        else:
            logging.info("Starting run loop")
            mc.start()


    logging.info(" ")
    logging.info("OK")
    logging.info("Shutting down")
    mc.stop()
    del controllers

    sys.exit(0)
