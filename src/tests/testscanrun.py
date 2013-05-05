'''
Created on Apr 9, 2013

@author: mikael
'''
import os
import sys

import recipelistmgr
import ctrl
import dataMemcache


def getBSMXfile():
    """ Get recipe list in test directory, and return filename"""
    rl = recipelistmgr.recipeListClass()
    cp = os.getcwd()
    try:
        filename = cp + '/Cloud.bsmx'
        print filename
        rl.readBeerSmith(filename)
    except:
        try:
            filename = 'Cloud.bsmx'
            rl.readBeerSmith(filename)
        except:
            try:
                filename = 'src/tests/Cloud.bsmx'
                rl.readBeerSmith(filename)
            except:
                print "Could not find test file"
                print os.getcwd()
                sys.exit(1)
    return(filename)


def test1():
    sr = ctrl.scanrun(getBSMXfile())
    assert sr.getRecipeList().len() > 1


def test2():
    """
    This is a very slow test as it goes through all the recipes
    in the cloud.bsmx file (in quick mode)
    """
    sr = ctrl.scanrun(getBSMXfile())
    rl = sr.getRecipeList()
    l = rl.getlist()
    d = dataMemcache.brewData()
    for key, recipe in l.items():
        print "=========", key
        d.setSelectedRecipe(key)
        d.setRunStatus('run')
        sr.runSelectedRecipe(True)
        print "xxxxxxxxxxx1"
        assert d.getRunStatus() == 'stop'


def test3():
    """
    Same as test2 but return after the first one is run.
    """
    sr = ctrl.scanrun(getBSMXfile())
    rl = sr.getRecipeList()
    l = rl.getlist()
    d = dataMemcache.brewData()

    for key, recipe in l.items():
        print "=========", key
        d.setSelectedRecipe(key)
        d.setRunStatus('run')
        sr.runSelectedRecipe(True)
        print "xxxxxxxxxxx1"
        assert d.getRunStatus() == 'stop'
        return

if __name__ == "__main__":
    test1()
    #test2()
    test3()
