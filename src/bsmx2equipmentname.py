#!/usr/bin/python
"""
Reads a beersmith recipe and creates stages file
Runs basic checks against controllers

"""

import sys
sys.path.append("/home/mikael/workspace/hoppity/src")
import ctrl
import argparse
import recipeReader
import json
import equipment
import os
import xml.etree.ElementTree
import checker
import logging

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Load files to S3')
    parser.add_argument('-i', '--inputfile', default=None, help='Input beersmith file')
    args = parser.parse_args()

    if args.inputfile is None:
        inf = sys.stdin
    else:
        try:
            inf = open(args.inputfile, 'r')
        except:
            print("Can not open inputfile")
            sys.exit(1)
    bsmxIn = inf.read()
    bsmxStr = bsmxIn.replace('&', 'AMP')
    inf.close()

    e = xml.etree.ElementTree.fromstring(bsmxStr)
    equipmentName = e.find('Data').find('Recipe').find('F_R_EQUIPMENT').find('F_E_NAME').text
    print('{}'.format(equipmentName))
