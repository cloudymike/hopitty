#!/bin/bash
source ./virtual.sh

export FN_AUTH_REDIRECT_URI=http://localhost:5000/google/auth
export FN_BASE_URI=http://localhost:5000
#export FN_AUTH_REDIRECT_URI=https://${C9_PID}.vfs.cloud9.us-east-1.amazonaws.com/google/auth
#export FN_BASE_URI=https://${C9_PID}.vfs.cloud9.us-east-1.amazonaws.com


#export FN_CLIENT_ID=
#export FN_CLIENT_SECRET=

export FLASK_DEBUG=1
export FN_FLASK_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

export IOT_CERT=$(cat $HOME/secrets/certs/e27d28a42b-certificate.pem.crt)
export IOT_PRIVATE=$(cat $HOME/secrets/keys/e27d28a42b-private.pem.key)

flask run
