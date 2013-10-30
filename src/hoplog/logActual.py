'''
Created on Sep 23, 2013

@author: mikael

This is probably not a logger but rather a plain file writer.
'''
import dataMemcache
import logging
import time
import datetime


class logActual():

    def __init__(self):
        self.data = dataMemcache.brewData()
        self.ctrls = self.data.getControllerList()
        self.oldstatus = ''
        self.oldControllers = None
        self.oldStage = None
        self.oldCurrentStage = None
        self.oldLineTime = datetime.datetime.now()

        # create logger, may not be used
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def outLine(self, message):
        # self.logger.info(message)
        now = datetime.datetime.now()
        print str(now) + message

    def headLine(self):
        message = ""
        for c in self.ctrls:
            message = message + ", " + c
        self.outLine(message)

    def logLine(self):
        status = self.data.getStatus()
        currentStage = self.data.getCurrentStage()
        controllers = status['controllers']
        elapsed = datetime.datetime.now() - self.oldLineTime
        if controllers != self.oldControllers:
            if currentStage != self.oldCurrentStage or \
               elapsed > datetime.timedelta(seconds=10):
                self.oldLineTime = datetime.datetime.now()
                message = ""
                for c in self.ctrls:
                    message = message + ", " + str(controllers[c]['actual'])
                self.outLine(message)
        self.oldControllers = controllers
        self.oldCurrentStage = currentStage

    def oneLine(self):
        runstatus = self.data.getRunStatus()
        if runstatus == 'run' and runstatus != self.oldstatus:
            self.headLine()
        else:
            self.logLine()
        self.oldstatus = runstatus

if __name__ == "__main__":
    l = logActual()
    while (1):
        l.oneLine()
        time.sleep(1)