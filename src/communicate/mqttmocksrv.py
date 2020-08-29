from __future__ import absolute_import
from __future__ import print_function
import argparse
from awscrt import io,auth, http
from awsiot import mqtt_connection_builder
from awscrt import mqtt as awsmqtt

import netsock
import time
from random import choice
from string import ascii_uppercase
import json
import argparse
import paho.mqtt.client as pahomqtt
import sys
import ssl
import logging, traceback
import os



IoT_protocol_name = "x-amzn-mqtt-ca"
aws_iot_endpoint = "a2d09uxsvr5exq-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

HOMEDIR=os.getenv("HOME")
ca = HOMEDIR+"/secrets/certs/awsrootca1.crt"
cert = HOMEDIR+"/secrets/certs/e27d28a42b-certificate.pem.crt"
private = HOMEDIR+"/secrets/keys/e27d28a42b-private.pem.key"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

def mkdata(length):
    growbig = 10 * length
    return(''.join(choice(ascii_uppercase) for i in range(growbig)))

class mockctrl():
    def __init__(self, args):
        self.count = 0
        self.state = 'stop'
        self.increment = 1

        # TODO parameterize the topic and host
        # TODO Break this out and pass do_command as a parameter.
        self.maintopic = 'topic'
        logger.info("start connect")

        if args.aws:
            # Spin up resources
            event_loop_group = io.EventLoopGroup(1)
            host_resolver = io.DefaultHostResolver(event_loop_group)
            client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
            self.client = mqtt_connection_builder.mtls_from_path(
                endpoint=aws_iot_endpoint,
                cert_filepath=cert,
                pri_key_filepath=private,
                ca_filepath=ca,
                client_bootstrap=client_bootstrap,
                client_id='hopitty')

            connect_future = self.client.connect()
            # Future.result() waits until a result is available
            connect_future.result()
            print("Connected!")

            # Subscribe
            subscribe_future, packet_id = self.client.subscribe(
                topic=self.maintopic,
                qos=awsmqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_message)

            subscribe_result = subscribe_future.result()
            print("Subscribed with {}".format(str(subscribe_result['qos'])))

        if args.mqtt:
            self.client = pahomqtt.Client("hwctrl")
            self.client.connect("localhost",1883,60)

            logger.info("connect success")

            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message

            self.client.loop_start()
            
      # Create an initial status. No stages, just state is stop
        init_status={}
        init_status['state'] = self.state
        status = json.dumps(init_status)
        print(status)
        self.set_status(status)


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
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
            print(status_string)
            self.stages = json.loads(status_string)
            self.state = 'stop'


    def set_status(self, message):
        topic = self.maintopic+"/status"
        if args.mqtt:
            self.client.publish(topic, message)
        else:
            self.client.publish(topic, message, qos=awsmqtt.QoS.AT_LEAST_ONCE)

        return()

    def run(self):
        for stage_name, stage in sorted(self.stages.items()):
            print("New stage: {}".format(stage_name))
            self.count = 0
            cycles = int(stage['cycles'])
            while self.count < cycles:
                statusdict = {}
                statusdict['state'] = self.state
                statusdict['stage'] = stage_name

                cyclestatus = {}
                cyclestatus['actual'] = self.count
                cyclestatus['target'] = cycles
                cyclestatus['targetMet'] = self.count >= cycles
                cyclestatus['powerOn'] = self.count < cycles
                cyclestatus['unit'] = 'U'
                ctrlstatus = {}
                ctrlstatus['cycles'] = cyclestatus
                statusdict['status'] = ctrlstatus
                status = json.dumps(statusdict)
                print(status)
                self.set_status(status)

                # This would be the actual activity
                time.sleep(1)
                if self.state != 'pause':
                    self.count = self.count + self.increment

                # Skip a step and return to run
                if self.state in ['skip']:
                    self.state = 'run'
                    break

                if self.state in ['stop', 'terminate']:
                    print('Stop, shutdown stages run')
                    return()



    def start(self):
        while 1:

            mystatus={}
            mystatus['state'] = self.state
            status = json.dumps(mystatus)
            #print(status)
            self.set_status(status)
            time.sleep(1)

            if self.state in ['run']:
                print('New set of stages')
                self.run()

            if self.state == 'terminate':
                return()
            # If stages ended, set state to stop
            if self.state != 'stop':
                self.state = 'stop'


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')
    args = parser.parse_args()

    if args.netsock:
        print("Not usable for netsock")
        sys.exit(1)

    mc = mockctrl(args)
    mc.start()

    mc.stop()
    print('Program ending')
