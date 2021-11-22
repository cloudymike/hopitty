#!/bin/bash
source $HOME/secrets//googauth.sh
LAMBDAENV="{
  FN_BASE_URI=https://brew.hopitty.com,
  FN_AUTH_REDIRECT_URI=https://brew.hopitty.com/google/auth,
  FN_CLIENT_ID=${FN_CLIENT_ID},
  FN_CLIENT_SECRET=${FN_CLIENT_SECRET},
  IOT_CERT=$(cat $HOME/secrets/certs/e27d28a42b-certificate.pem.crt),
  IOT_PRIVATE=$(cat $HOME/secrets/keys/e27d28a42b-private.pem.key)
}"

aws lambda update-function-configuration --function-name hopfront-app-dev --environment "Variables=${LAMBDAENV}"
