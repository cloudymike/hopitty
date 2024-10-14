#!/bin/bash

# Check the requirements list
# virtualenv might be good





export FN_AUTH_REDIRECT_URI=http://localhost:8080/google/auth
export FN_BASE_URI=http://localhost:8080
#export FN_AUTH_REDIRECT_URI=https://${C9_PID}.vfs.cloud9.us-east-1.amazonaws.com/google/auth
#export FN_BASE_URI=https://${C9_PID}.vfs.cloud9.us-east-1.amazonaws.com


#export FN_CLIENT_ID=
#export FN_CLIENT_SECRET=

export FLASK_DEBUG=1
export FN_FLASK_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

# Required for dynamodb, just dummy vars
export AWS_ACCESS_KEY_ID='DUMMYIDEXAMPLE'
export AWS_SECRET_ACCESS_KEY='DUMMYEXAMPLEKEY'
export REGION='us-west-2'

python3 ./web.py -H 192.168.62.151 -D "http://192.168.62.151:8000"
