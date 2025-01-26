#!/bin/bash

# These are steps to setup a virtual environment to work with python2
# Run all programs (using python2 at least) in this environment
# If something is missing, go back to setup and find commands required

# Remove whatever is there
rm -rf venv

# Start a fresh setup
virtualenv -p python2 venv

# This will need to be redone again after script is done
source venv/bin/activate

pushd phidget/PhidgetsPython/
python2 setup.py install
popd

pip install --upgrade pip
pip install --upgrade setuptools wheel 

pip install -r requirements.txt

