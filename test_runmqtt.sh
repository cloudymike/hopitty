#!/bin/bash

echo Make shore the mqtt broker is running locally
echo sudo service mosquitto start

timeout 300 src/runmqtt.py -m &
sleep 9
python src/communicate/tstrunmqtt.py -m
sleep 1
kill -9 %1
kill -9 $(pgrep runmqtt)
