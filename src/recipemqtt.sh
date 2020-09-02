#!/bin/bash
# Script to read in a recipe, and then create a json stages and run runmqtt with it
# Mainly for testing

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

OPTIONS=''
while getopts "f:qc" opt; do
  case ${opt} in
    f ) INFILE=$OPTARG
      ;;
    q ) OPTIONS=$OPTIONS' -q'
      ;;
    c ) OPTIONS=$OPTIONS' -c'
      ;;
  esac
done

TMPFILENAME='/tmp/'$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

$DIR/json2stages.py -i $INFILE -o $TMPFILENAME -e 'Grain 3G, 5Gcooler, 5Gpot, platechiller'
$DIR/runmqtt.py -n -r $TMPFILENAME -t 'Grain 3G, 5Gcooler, 5Gpot, platechiller' $OPTIONS

rm $TMPFILENAME
