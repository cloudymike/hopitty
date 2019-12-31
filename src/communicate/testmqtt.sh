#!/bin/bash

timeout 60 python ./mqttmocksrv.py -m &
sleep 1
python ./mockclient.py -m

# Check if mocksrv.py is running, if so forcefully kill it
if $(pgrep mqttmocksrv.py  -n &> /dev/null)
then 
  pkill -9 "python ./mqttmocksrv.py"
  exit 1
fi
