#!/bin/bash
source ./virtual.sh
zappa deploy
zappa unschedule
zappa certify
