#!/bin/bash
docker build --target local -f ./beachbooker/Dockerfile -t 082113759242.dkr.ecr.eu-central-1.amazonaws.com/beachbooker-lambda:latest .
docker run 082113759242.dkr.ecr.eu-central-1.amazonaws.com/beachbooker-lambda:latest
