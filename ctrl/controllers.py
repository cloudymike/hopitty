#!/usr/bin/python
    
    
class controllers(dict):
    def __init__(self):
        pass  

    def addController(self,ctrl):
        self[ctrl.__class__.__name__] = ctrl
    
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
            curr['actual'] = c.get()
            curr['target'] = c.getTarget()
            curr['unit'] = c.getUnit()
            curr['powerOn'] = c.getPowerOn()
            curr['targetMet'] = c.targetMet()
            ctrlStat[key] = curr
        return ctrlStat
    
 
c = controllers()   
