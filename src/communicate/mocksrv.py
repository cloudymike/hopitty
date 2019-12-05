import netsock
import time


class mockctrl():
    def __init__(self):
        self.count = 0
        self.state = 'stop'
        self.increment = 0
        self.sc = netsock.socketcomm()
    
    def start(self):
        while 1:
            status = "state: {}      count: {}".format(self.state, self.count)
            command = self.sc.readSocket(status)
            print("Command {}".format(command))
            if 'terminate' in command:
                self.sc.close()
                return()
            if 'run' in command:
                self.increment = 1
                self.state = 'run'
            if 'stop' in command:
                self.increment = 0
                self.state = 'stop'
            if 'pause' in command:
                self.state = 'pause'
                self.increment = 0

            self.count = self.count + self.increment

            time.sleep(1)

if __name__ == "__main__":
    
#    sc = netsock.socketcomm()
#    while 1:
#        data = sc.readSocket('All OK')
#        print("Doing stuff with {}".format(data))
#        time.sleep(1)
    mc = mockctrl()
    mc.start()
    print('Program ending')
