
import appliances.myloader
import threading
import time
import datetime

STRESSTEST = False


class controllerList(dict):
    def __init__(self, useHWlock=True):
        self.useHWlock = useHWlock
        # Lock the hardware anytime it is accessed
        if self.useHWlock:
            self.HWlock = threading.RLock()

        self.mylog = {}

        if STRESSTEST:
            print("WARNING: Running in stress test mode")

    def setEquipment(self,equipment):
        """
        Set the equipement name to allow identify
        multiple setups and check reciepes against them
        """
        # This needs to be stored somewhere
        # As this is a list, no space in the object
        # Could fake it but storing it in the delayTimer as that one is always there.
        # The setup will need to define these anyhow.
        # We could even add delay timer at init.
        pass

    def getEquipmentName(self):
        """
        Get the equiment type the controller is setup as.
        Allow to check recipe against the setup
        """
        return(self['controllerInfo'].getEquipmentName())

    def getEquipment(self):
        """
        Return the equipement data required to check recipe against
        """
        return(self['controllerInfo'].getEquipment())

    def getEquipmentSpecs(self):
        """
        Return the equipement data required to check recipe against
        """
        return(self['controllerInfo'].getEquipmentSpecs())

    def addController(self, name, ctrl):
        self[name] = ctrl

    def addControllerList(self, l):
        if self.useHWlock:
            self.HWlock.acquire()
        for className, instance in l.items():
            self.addController(className, instance)
        if self.useHWlock:
            self.HWlock.release()

    def load(self):
        """
        This should really be init, but is left as a function until all
        other calls to controllers are rewritten
        """
        if self.useHWlock:
            self.HWlock.acquire()
        l = appliances.myloader.myQuickLoader()
        l.build()
        self.addControllerList(l.instances())
        if self.useHWlock:
            self.HWlock.release()

    def shutdown(self):
        """
        Shutdown the controllers
        This means removing them from the list and destroying them
        The controllers should also be stopped
        """

        if self.useHWlock:
            self.HWlock.acquire()

        # Clumsy but Python3 can not deal with removing while iterating
        keylist=[]
        for key, c in self.items():
            keylist.append(key)
        for key in keylist:
            c = self[key]
            c.stop()
            del self[key]
            del c
        if self.useHWlock:
            self.HWlock.release()

    def stop(self):
        """Stop all controllers"""
        if self.useHWlock:
            self.HWlock.acquire()
        for c in self.values():
            c.stop()
        if self.useHWlock:
            self.HWlock.release()

    def HWOK(self):
        """
        Check if all HW is connected and if not, return
        False.
        On Failure, list what appliances are OK and failing.
        """
        if self.useHWlock:
            self.HWlock.acquire()
        usbOK = True
        for c in self.values():
            if not c.HWOK():
                usbOK = False
        if not usbOK:
            print("--------- Hardware status ---------")
            for key, c in self.items():
                if c.HWOK():
                    print("    OK:  ", key)
                else:
                    print("    Fail:", key)
            print("-----------------------------------")
        if self.useHWlock:
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
        if self.useHWlock:
            self.HWlock.acquire()
        for key, c in self.items():
            if not self.useHWlock:
                c.measure()
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.pause()
                c.update()
        if self.useHWlock:
            self.HWlock.release()

    def run(self, settings):
        """
        Run all controllers
        Take a measure, check settings and update controllers
        """
        if self.useHWlock:
            self.HWlock.acquire()
        for key, c in self.items():
            # measure once cut twice...this will read sensors, and store value
            if not self.useHWlock:
                c.measure()
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.start()
                c.update()
        if self.useHWlock:
            self.HWlock.release()

    def stopCurrent(self, settings):
        """
        Stops controllers that are currently in the stage
        Significant speedup for quickRecipe
        """
        if self.useHWlock:
            self.HWlock.acquire()
        for key, c in self.items():
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.stop()
        if self.useHWlock:
            self.HWlock.release()

    def measureSensors(self):
        """
        Use measure to pull all sensors
        Do this once pe cycle, then all other sensor values could be
        pulled from stored value
        """
        for key, c in self.items():
            c.measure()
        return

    def status(self):
        """
        Save the status of the controller in a dictionary
        Uses get to read the sensors directly (expensive)
        """
        if self.useHWlock:
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
            ctrlStat[key] = curr
        if self.useHWlock:
            self.HWlock.release()
        return ctrlStat

    def stage_template(self, stagename):
        """
        Return a stage template for current controller
        """
        stage={}
        ctrlStat = {}
        for key, c in self.items():
            curr = {}
            curr['active'] = False
            curr['targetValue'] = 0
            ctrlStat[key] = curr
        stage[stagename] = ctrlStat
        return stage

    def statusAppliance(self, key):
        """
        Save the status of one of the appliances in the controller in a dictionary
        """
        if self.useHWlock:
            self.HWlock.acquire()
        c = self[key]
        curr = {}
        curr['active'] = c.isActive()
        curr['actual'] = c.get()
        curr['target'] = c.getTarget()
        curr['unit'] = c.getUnit()
        curr['powerOn'] = c.getPowerOn()
        curr['targetMet'] = c.targetMet()
        if self.useHWlock:
            self.HWlock.release()
        return curr

    def lightStatusAppliance(self, key):
        """
        Save the status of one of the appliances in the controller in a dictionary
        In this case use light version, get value but don't remeasure
        """
        c = self[key]
        curr = {}
        curr['active'] = c.isActive()
        curr['actual'] = c.getActualVar()
        curr['target'] = c.getTarget()
        curr['unit'] = c.getUnit()
        curr['powerOn'] = c.getPowerOn()
        curr['targetMet'] = False
        return curr

    def lightStatus(self):
        """
        Save the status of the controller in a dictionary
        Lightweight version, do not re-measure
        """
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
        if self.useHWlock:
            self.HWlock.acquire()
        t = datetime.datetime.now().time()
        ctrlStat = str(t)
        for key, c in self.items():
            ctrlStat = ctrlStat + "," + str(c.getActualVar())
        if self.useHWlock:
            self.HWlock.release()
        return ctrlStat

    def csvheader(self):
        """
        Save the values of the controller names as header
        """
        if self.useHWlock:
            self.HWlock.acquire()
        ctrlStat = "Time"
        for key, c in self.items():
            ctrlStat = ctrlStat + "," + key
        if self.useHWlock:
            self.HWlock.release()
        return ctrlStat

    def done(self):
        if self.useHWlock:
            self.HWlock.acquire()
        alldone = True
        for key, c in self.items():
            if c.isActive():
                alldone = alldone and c.targetMet()
        if self.useHWlock:
            self.HWlock.release()
        return(alldone)
