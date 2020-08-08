#!/bin/bash
pushd ..
timeout 300 ./runmqtt.py -m &
popd
sleep 9
python ./tstrunmqtt.py -m
sleep 1
kill -9 %1
kill -9 $(pgrep runmqtt)
