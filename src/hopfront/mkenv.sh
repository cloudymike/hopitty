#!/bin/bash

virtualenv -p python3 venv
source venv/bin/activate
echo $VIRTUAL_ENV
pip install -r requirements.txt
echo "==============================="
echo "source venv/bin/activate"
