#!/bin/bash

# Need context from directory above.
docker build ../.. --file Dockerfile -t onlinebeersmith
docker kill obs
docker rm obs
docker run --name obs onlinebeersmith