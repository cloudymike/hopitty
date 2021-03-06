import netsock
import time
from random import choice
from string import ascii_uppercase
import json
import argparse


def mkdata(length):
    growbig = 10 * length
    return(''.join(choice(ascii_uppercase) for i in range(growbig))) 

class mockctrl():
    def __init__(self, comm2use):
        self.count = 0
        self.state = 'stop'
        self.increment = 0
        self.sc = comm2use
        
        self.hold_forever = {}
        self.hold_forever['holdforever'] = {}
        self.hold_forever['holdforever']['cycles'] = 500000
        self.stages = self.hold_forever

    
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
                    if args.netsock:
                        self.sc.set_status(status)
                        command, data = self.sc.get_command()
                    if command == 'terminate':
                        self.sc.close()
                        return()
                    if command == 'run':
                        self.increment = 1
                        self.state = 'run'
                    if command == 'stop':
                        self.increment = 0
                        self.state = 'stop'
                        self.stages = self.hold_forever
                        break
                    if command == 'pause':
                        self.state = 'pause'
                        self.increment = 0
                    if command == 'loading':
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
    if args.mqtt:
        pass
    mc = mockctrl(comm2use)

    
    mc.start()
    print('Program ending')
