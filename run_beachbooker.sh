#!/bin/bash
docker build --target local -f ./beachbooker/Dockerfile -t beachbooker .
docker run beachbooker
