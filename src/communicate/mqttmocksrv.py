import netsock
import time
from random import choice
from string import ascii_uppercase
import json
import argparse
import paho.mqtt.client as mqtt


def mkdata(length):
    growbig = 10 * length
    return(''.join(choice(ascii_uppercase) for i in range(growbig))) 

class mockctrl():
    def __init__(self, comm2use=None):
        self.count = 0
        self.state = 'stop'
        self.increment = 0
        self.sc = comm2use
        self.command = ""
        
        self.hold_forever = {}
        self.hold_forever['holdforever'] = {}
        self.hold_forever['holdforever']['cycles'] = 500000
        self.stages = self.hold_forever
        
        self.maintopic = 'topic'
        self.client = mqtt.Client("hwctrl")
        self.client.connect("localhost",1883,60)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("topic/test")

    def on_message(self, client, userdata, msg):
        self.command = msg.payload.decode()

    def set_status(self, message):
        topic = self.maintopic+"/status"
        self.client.publish(topic, message)
        return()

    
    def start(self):
        while 1:
            print('New set of stages')
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
                    cyclestatus['powerOn'] = self.increment > 0
                    cyclestatus['unit'] = 'U'
                    ctrlstatus = {}
                    ctrlstatus['cycles'] = cyclestatus
                    statusdict['status'] = ctrlstatus

                    status = json.dumps(statusdict)
                    print(status)
                    
                    self.set_status(status)
                    #command, data = self.sc.get_command()
                    if self.command == 'terminate':
                        self.command = ""
                        self.client.loop_stop()
                        return()
                    if self.command == 'run':
                        self.command = ""
                        self.increment = 1
                        self.state = 'run'
                    if self.command == 'stop':
                        self.command = ""
                        self.increment = 0
                        self.state = 'stop'
                        self.stages = self.hold_forever
                        break
                    if self.command == 'pause':
                        self.command = ""
                        self.state = 'pause'
                        self.increment = 0
                    if len(self.command) > 0 and self.command[0] == '{':
                        data = self.command
                        self.command = ""
                        status_string = str(data).replace("'","")
                        print(status_string)
                        self.stages = json.loads(status_string)
                        
                        self.increment = 0
                        self.state = 'stop'
                        break
        
                    # This would be the actual activity
                    if self.state != 'stop':
                        self.count = self.count + self.increment
        
                    time.sleep(1)
                    
                if self.state in ['stop']:
                    break

            if self.state != 'stop':
                self.state = 'stop'
                self.stages = self.hold_forever
           

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    args = parser.parse_args()
    
    if args.netsock:
        comm2use = netsock.socketcomm()
    mc = mockctrl()

    
    mc.start()
    print('Program ending')
