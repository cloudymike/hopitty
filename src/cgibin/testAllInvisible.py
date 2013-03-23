# TODO this is not working
# cgi-bin is not a valid module


import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/cgi-bin")

import dataMemcache

import startreader
import recipereader


def teststartreader():
    startreader.startreaderMain()
    myData = dataMemcache.brewData()
    runStatus = myData.getRunStatus()
    assert isinstance(runStatus, str)
    print runStatus


def testrecipereader():
    recipereader.recipereaderMain()
    myData = dataMemcache.brewData()
    cr = myData.getSelectedRecipe()
    assert isinstance(cr, str)
    print cr

if __name__ == "__main__":
    teststartreader()
