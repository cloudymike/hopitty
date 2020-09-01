#!/bin/bash

# Starts a mock server and then the web server to test against
# Runs for 5 min and then dies

timeout 300 python ../communicate/mqttmocksrv.py -m &
sleep 1

timeout 300  ./run.sh
