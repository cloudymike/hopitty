import netsock
import time
from random import choice
from string import ascii_uppercase
import json


def mkdata(length):
    growbig = 10 * length
    return(''.join(choice(ascii_uppercase) for i in range(growbig))) 

class mockctrl():
    def __init__(self):
        self.count = 0
        self.state = 'stop'
        self.increment = 0
        self.sc = netsock.socketcomm()
        
        self.hold_forever = {}
        self.hold_forever['holdforever'] = {}
        self.hold_forever['holdforever']['cycles'] = 5000
        self.stages = self.hold_forever

    
    def start(self):
        while 1:
            print('New set of stages')
            for stage_name, stage in sorted(self.stages.items()):
                print("New stage: {}".format(stage_name))
                self.count = 0
                cycles = int(stage['cycles'])
                while self.count < cycles:
                    status = "state: {}, stage: {} count: {} data: {} ".format(self.state, stage_name, self.count, mkdata(3))
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
    
    mc = mockctrl()
    mc.start()
    print('Program ending')
