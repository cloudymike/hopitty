


# Docker howto


## Status
The app works in docker connecting to AWS, using the script rundocker.sh

Latest dynamodb does not work on docker, but works as a local java program and can be used as such for development. The easiest is to run script in src/dynamo:

`
 ./run.sh -l -t "Grain 3G, 5Gcooler, 5Gpot, mashexittemp"

`

Alternative is to run dynamodb with older version. V1.20 work:
`
docker run -p 8000:8000 amazon/dynamodb-local:1.20.0
`
