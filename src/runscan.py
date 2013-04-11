#!/usr/bin/python
"""
Scans the recipe database and creates recipeListClass object
Also pushes recipe name list to memcache for use by web pages

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src") 
sys.path.append("/home/mikael/workspace/hoppity/src/recipelistmgr")
import getpass
import os
import recipelistmgr
import time
import ctrl
import dataMemcache

user = 'mikael'


def run(mydata):
    rs = mydata.getRunStatus()
    if rs == 'run':
        return(True)
    else:
        return(False)

def runscan(runOnce = False):
    """
    Run loop, the daemon that will be running forever
    For testing purposes we can run in one shot mode.
    When doing this first write data to dataMemcache and then
    run through once.
    """
    print "Alive"
    rl = recipelistmgr.recipeListClass()
    mydata = dataMemcache.brewData()
    loop = True
    mydata.setRunStatus('stop')
    while loop:
        bsmxfile = "/home/"+user+"/.beersmith2/Cloud.bsmx"
        rl.readBeerSmith(bsmxfile)
        rl.nameListToMemcache()
        print rl.len()

        if run(mydata):
            r = rl.getRecipe(mydata.getSelectedRecipe())
            if r != None:
                bsxml = r.getBSMXdoc()
                ru = ctrl.rununit()
                ru.bsmxIn(bsxml)
                runOK = ru.run()
                if not runOK:
                    print "Run failed"
                del ru
                mydata.setRunStatus('stop')
        time.sleep(2)
        if runOnce:
            loop = False
        
if __name__ == "__main__":
    oldstyle = False
    if oldstyle:
        runscan()
    else:
        daemon = ctrl.scanrun()
        daemon.loop()
        