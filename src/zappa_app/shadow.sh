#!/bin/bash


python shadow.py \
   --endpoint a2d09uxsvr5exq-ats.iot.us-east-1.amazonaws.com \
   --root-ca /home/mikael/secrets/certs/awsrootca1.crt \
   --cert /home/mikael/secrets/certs/e27d28a42b-certificate.pem.crt \
   --key /home/mikael/secrets/keys/e27d28a42b-private.pem.key \
   --thing-name hopitty \
