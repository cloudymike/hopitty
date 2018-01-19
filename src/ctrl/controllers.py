
import appliances.myloader
import threading
import time
import datetime

STRESSTEST = False


class controllerList(dict):
    def __init__(self):
        # Lock the hardware anytime it is accessed
        self.HWlock = threading.RLock()
        #self.HWlock.release()
        self.mylog = {}

        if STRESSTEST:
            print "WARNING: Running in stress test mode"

    def addController(self, name, ctrl):
        #print "Adding ", name
        self[name] = ctrl

    def addControllerList(self, l):
        self.HWlock.acquire()
        for className, instance in l.iteritems():
            self.addController(className, instance)
        self.HWlock.release()

    def load(self):
        """
        This should really be init, but is left as a function until all
        other calls to controllers are rewritten
        """
        self.HWlock.acquire()
        l = appliances.myloader.myQuickLoader()
        l.build()
        self.addControllerList(l.instances())
        self.HWlock.release()

    def shutdown(self):
        """
        Shutdown the controllers
        This means removing them from the list and destroying them
        The controllers should also be stopped
        """

        self.HWlock.acquire()
        for key, c in self.items():
            c.stop()
            del self[key]
            del c
        self.HWlock.release()

    def stop(self):
        """Stop all controllers"""
        self.HWlock.acquire()
        for c in self.itervalues():
            c.stop()
        self.HWlock.release()

    def HWOK(self):
        """
        Check if all HW is connected and if not, return
        False.
        On Failure, list what appliances are OK and failing.
        """
        self.HWlock.acquire()
        usbOK = True
        for c in self.itervalues():
            if not c.HWOK():
                usbOK = False
        if not usbOK:
            print "--------- Hardware status ---------"
            for key, c in self.items():
                if c.HWOK():
                    print "    OK:  ", key
                else:
                    print "    Fail:", key
            print "-----------------------------------"
        self.HWlock.release()
        return(usbOK)

    def check(self, settings):
        """
        Check all controllers
        Take a measure, check settings and update controllers
        """
        ctrl_lst = []
        recipe_lst = []
        for key, c in self.items():
            ctrl_lst.append(key)
        for key, c in settings.items():
            recipe_lst.append(key)
            try:
                index = ctrl_lst.index(key)
            except:
                return(False)
        return(True)

    def pause(self, settings):
        """
        Run all controllers
        Take a measure, check settings and update controllers
        """
        self.HWlock.acquire()
        for key, c in self.items():
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.pause()
                c.update()
        self.HWlock.release()

    def run(self, settings):
        """
        Run all controllers
        Take a measure, check settings and update controllers
        """
        self.HWlock.acquire()
        for key, c in self.items():
#            if not STRESSTEST:
#                time.sleep(0.01)
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.start()
                c.update()
            # This is not needed as we stop all controllers at
            # beginning of each stage. It is also very time
            # consuming as most controllers are not in use
            # in each stage
            # else:
                if STRESSTEST:
                    c.stop()
        self.HWlock.release()

    def stopCurrent(self, settings):
        """
        Stops controllers that are currently in the stage
        Significant speedup for quickRecipe
        """
        self.HWlock.acquire()
        for key, c in self.items():
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.stop()
        self.HWlock.release()

    def status(self):
        """
        Save the status of the controller in a dictionary
        """
        self.HWlock.acquire()
        ctrlStat = {}
        for key, c in self.items():
            curr = {}
            curr['active'] = c.isActive()
            curr['actual'] = c.get()
            curr['target'] = c.getTarget()
            curr['unit'] = c.getUnit()
            curr['powerOn'] = c.getPowerOn()
            curr['targetMet'] = c.targetMet()
        self.HWlock.release()
        return curr

    def statusAppliance(self, key):
        """
        Save the status of one of the appliances in the controller in a dictionary
        """
        self.HWlock.acquire()
        c = self[key]
        curr = {}
        curr['active'] = c.isActive()
        curr['actual'] = c.get()
        curr['target'] = c.getTarget()
        curr['unit'] = c.getUnit()
        curr['powerOn'] = c.getPowerOn()
        curr['targetMet'] = c.targetMet()
        self.HWlock.release()
        return curr

    def lightStatus(self):
        """
        Save the status of the controller in a dictionary
        Lightweight version, do not re-measure
        """
        #self.HWlock.acquire()
        ctrlStat = {}
        for key, c in self.items():
            curr = {}
            curr['active'] = c.isActive()
            curr['actual'] = c.getActualVar()
            curr['target'] = c.getTarget()
            curr['unit'] = c.getUnit()
            curr['powerOn'] = c.getPowerOn()
            curr['targetMet'] = False
            ctrlStat[key] = curr
        #self.HWlock.release()
        return ctrlStat

    def logstatus(self):
        """
        Add status to mylog dictionary with a timestamp as key
        """
        t = datetime.datetime.now()
        self.mylog[t] = self.status()

    def getMyLog(self):
        return self.mylog

    def csv(self):
        """
        Save the status of the controller in a csv line
        """
        self.HWlock.acquire()
        t = datetime.datetime.now().time()
        ctrlStat = str(t)
        for key, c in self.items():
            ctrlStat = ctrlStat + "," + str(c.getActualVar())
        self.HWlock.release()
        return ctrlStat

    def csvheader(self):
        """
        Save the values of the controller names as header
        """
        self.HWlock.acquire()
        ctrlStat = "Time"
        for key, c in self.items():
            ctrlStat = ctrlStat + "," + key
        self.HWlock.release()
        return ctrlStat

    def done(self):
        self.HWlock.acquire()
        alldone = True
        for key, c in self.items():
            if c.isActive():
                alldone = alldone and c.targetMet()
        self.HWlock.release()
        return(alldone)
