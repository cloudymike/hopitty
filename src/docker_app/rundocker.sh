#! /bin/bash

docker build . -t brew
docker run -p 8080:8080 brew
