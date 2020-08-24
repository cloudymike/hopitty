#!/bin/bash
source ./virtual.sh
zappa deploy
zappa unschedule
