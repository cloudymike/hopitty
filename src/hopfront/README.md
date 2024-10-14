

Docker work but not docker compose with dynamodb
docker compose works with only hopfront and hardcoded IP

Ugly hardcoded IPs in dockerfile but will not be needed when docker compose works

dynamodb issues with dockercompose, i.e. when dynamodb runs in docker web app can not reach it.
Maybe simplify the whole setup, too many varaible passed as options
It does work in the docker branch so go figure.



To run:

### Window 1
cd hopitty
source venv/bin/activate
cd src/dynamo
./run.sh -l


### Window 2
cd hopitty
source venv/bin/activate
cd src
python runmqtt.py -H localhost -t "Grain 3G, 5Gcooler, 5Gpot, mashexittemp" -s

### Window 3
cd hopitty/src/hopfront
docker compose up

Note to run just with docker instead use
./rundocker.sh
