'''
Created on Sep 23, 2013

@author: mikael
'''
import dataMemcache
import logging


class logActual():

    def __init__(self):
        self.data = dataMemcache.brewData()
        self.ctrls = self.data.getControllerList()

        # create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        # formatter = logging.Formatter('%(asctime)s - %(name)s -
        #                                %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

    def headLine(self):
        message = ""
        for c in self.ctrls:
            message = message + ", " + c
        self.logger.info(message)

    def logLine(self):
        message = ""
        status = self.data.getStatus()
        controllers = status['controllers']

        for c in self.ctrls:
            message = message + ", " + str(controllers[c]['actual'])
        self.logger.info(message)

if __name__ == "__main__":
    l = logActual()
    l.headLine()
    l.logLine()
