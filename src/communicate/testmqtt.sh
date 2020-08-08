#!/bin/bash

timeout 60 python ./mqttmocksrv.py -m &
sleep 1
python ./mockclient.py -m | cat
sleep 1
kill -9 %1
#kill -9 $(pgrep mqttmocksrv)
