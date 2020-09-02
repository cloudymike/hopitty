#!/bin/bash
# Script to read in a recipe, and then create a json stages and run runmqtt with it
# Mainly for testing
if [ "$1" == "" ]
then
  echo "USAGE: $0 recipefile"
  exit 1
fi

TMPFILENAME='/tmp/'$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

./json2stages.py -i $1 -o $TMPFILENAME -e 'Grain 3G, 5Gcooler, 5Gpot, platechiller'
./runmqtt.py -n -r $TMPFILENAME -t 'Grain 3G, 5Gcooler, 5Gpot, platechiller'
