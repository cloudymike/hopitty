#!/bin/bash

export IOT_CERT=$(cat $HOME/secrets/certs/e27d28a42b-certificate.pem.crt)
export IOT_PRIVATE=$(cat $HOME/secrets/keys/e27d28a42b-private.pem.key)

python command.py -c $1
