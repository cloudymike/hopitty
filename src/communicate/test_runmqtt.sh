#!/bin/bash
pushd ..
timeout 60 ./runmqtt.py -m &
popd
sleep 5
python ./test_runmqtt.py -m
sleep 1
kill -9 %1
kill -9 $(pgrep runmqtt)
