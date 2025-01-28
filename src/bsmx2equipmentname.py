#!/usr/bin/python
"""
Reads a bsmx file and displays equipment name
Runs basic checks against controllers

"""

import sys
import argparse
import json
import os
import xml.etree.ElementTree
import logging

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Reads a bsmx file and displays equipment name')
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
