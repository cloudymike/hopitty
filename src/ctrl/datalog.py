import ctrl
import threading
import time


class datalogger(threading.Thread):

    def __init__(self, controllers=None, filename='/tmp/brewlog.csv'):
        """
        Run equipment in controllers based on json file provided
        """
        super(datalogger, self).__init__()
        self.controllers = controllers
        self._stopflag = threading.Event()
        self.filename = filename

    def run(self):
        self._stopflag.clear()
        datafile = open(self.filename, 'w', 1)
        datafile.write(self.controllers.csvheader() + "\n")
        while not self._stopflag.isSet():
            datafile.write(self.controllers.csv() + "\n")
            time.sleep(5)
        datafile.close()

    def stop(self):
        self._stopflag.set()
