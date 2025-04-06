#!/bin/bash
docker build --target base -f ./beachbooker/Dockerfile -t 082113759242.dkr.ecr.eu-central-1.amazonaws.com/beachbooker-lambda:latest .
docker push 082113759242.dkr.ecr.eu-central-1.amazonaws.com/beachbooker-lambda:latest
