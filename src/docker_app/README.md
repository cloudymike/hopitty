


# Docker howto


## Status
The app works in docker connecting to AWS, using the script rundocker.sh

dynamodb does not work on docker, but works as a local java program and can be used as such for development. The easiest is to run script in src/dynamo:

`
 ./run.sh -l -t "Grain 3G, 5Gcooler, 5Gpot, mashexittemp"

`

