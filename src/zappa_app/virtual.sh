#!/bin/bash
if [ "$VIRTUAL_ENV" == "" ]
then
  virtualenv -p python3 venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  echo Virtual env already installed in $VIRTUAL_ENV
fi
