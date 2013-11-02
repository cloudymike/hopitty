#!/usr/bin/python

# branch t1
import sys
import time
sys.path.append("/home/mikael/workspace/hoppity/src")
sys.path.append("/home/mikael/workspace/hoppity/src/appliances")
sys.path.append("/home/mikael/workspace/hoppity/src/ctrl")

import getopt
import ctrl
import dataMemcache




if __name__ == "__main__":

    data = dataMemcache.brewData()
    while True:
        data.unsetError()
        data.setPause(False)
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
