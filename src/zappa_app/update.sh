#!/bin/bash
source ./virtual.sh
zappa update
zappa unschedule
zappa certify
