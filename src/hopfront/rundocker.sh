#/bin/bash

docker build . -t hopfront
docker run -p 8080:8080 hopfront

