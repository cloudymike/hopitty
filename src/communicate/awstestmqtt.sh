#!/bin/bash
# This is NOT included in automatic tests as it requires secrets.
# Use localhost testing instead.

timeout 60 python ./mqttmocksrv.py -a &
sleep 1
python ./mockclient.py -a

# Check if mocksrv.py is running, if so forcefully kill it
if $(pgrep mqttmocksrv.py  -n &> /dev/null)
then 
  pkill -9 "python ./mqttmocksrv.py"
  exit 1
fi
echo SUCCESS