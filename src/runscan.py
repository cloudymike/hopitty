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

     
if __name__ == "__main__":
    daemon = ctrl.scanrun()
    daemon.loop()
        