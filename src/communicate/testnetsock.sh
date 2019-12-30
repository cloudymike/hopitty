#!/bin/bash

timeout 60 python ./mocksrv.py &
sleep 1
python ./mockclient.py -n

# Check if mocksrv.py is running, if so forcefully kill it
if $(pgrep mocksrv.py  -n &> /dev/null)
then 
  pkill -9 "python ./mocksrv.py"
  exit 1
fi
