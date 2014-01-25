
import appliances.myloader
import time


class controllerList(dict):
    def __init__(self):
        pass

    def addController(self, name, ctrl):
        print "Adding ", name
        self[name] = ctrl

    def addControllerList(self, l):
        for className, instance in l.iteritems():
            self.addController(className, instance)

    def load(self):
        """
        This should really be init, but is left as a function until all
        other calls to controllers are rewritten
        """
        l = appliances.myloader.myQuickLoader()
        l.build()
        self.addControllerList(l.instances())

    def shutdown(self):
        """
        Shutdown the controllers
        This means removing them from the list and destroying them
        The controllers should also be stopped
        """
        for key, c in self.items():
            c.stop()
            del self[key]
            del c

    def stop(self):
        """Stop all controllers"""
        for c in self.itervalues():
            c.stop()

    def HWOK(self):
        """
        Check if all HW is connected and if not, return
        False.
        On Failure, list what appliances are OK and failing.
        """
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
        for key, c in self.items():
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.pause()
                c.update()

    def run(self, settings):
        """
        Run all controllers
        Take a measure, check settings and update controllers
        """
        for key, c in self.items():
            time.sleep(0.01)
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
            #    c.stop()

    def stopCurrent(self, settings):
        """
        Stops controllers that are currently in the stage
        Significant speedup for quickRecipe
        """
        for key, c in self.items():
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.stop()

    def status(self):
        """
        Save the status of the controller in a dictionary
        """
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
        return ctrlStat

    def done(self):
        alldone = True
        for key, c in self.items():
            if c.isActive():
                alldone = alldone and c.targetMet()
        return(alldone)
