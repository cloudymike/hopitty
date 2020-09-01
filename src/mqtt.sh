#!/bin/bash
# Runs the front end and backend for the mqtt based server
# For testing

# Starting mosquitto should not be needed but included for completeness
sudo service mosquitto start
pushd dynamo
./up.sh &
popd

export FN_AUTH_REDIRECT_URI=http://localhost:8080/google/auth
export FN_BASE_URI=http://localhost:8080
export FLASK_DEBUG=0
export FN_FLASK_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

pushd hopfront
python ./web.py -m &
popd

# Start backend
./runmqtt.py -m

# kill webserver
kill %1
kill %2
