import sys
import appliances.myloader


class controllerList(dict):
    def __init__(self):
        pass

    def addController(self, name, ctrl):
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

    def check(self, settings):
        """
        Run all controllers
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
                print "Recipe asks for missing controller", key
                print "Stopping"
                return(False)
        return(True)

    def run(self, settings):
        """
        Run all controllers
        Take a measure, check settings and update controllers
        """
        for key, c in self.items():
            s = settings[key]
            c.set(s['targetValue'])
            if s['active']:
                c.start()
                c.update()
            else:
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
