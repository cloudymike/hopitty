#!/bin/bash

timeout 60 python ./mocksrv.py &
sleep 1
python ./mockclient.py

pkill -9 "python ./mocksrv.py"
