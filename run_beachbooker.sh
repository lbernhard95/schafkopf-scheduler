#!/bin/bash
docker build --rm --target local -f ./beachbooker/Dockerfile -t beachbooker .
docker run beachbooker
