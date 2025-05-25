#!/bin/bash

sudo snap install aws-cli --classic
aws configure
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 240304666027.dkr.ecr.us-east-1.amazonaws.com
docker buildx build --platform linux/amd64 --provenance=false -t fbot-downdetector .
docker tag fbot-downdetector:latest  240304666027.dkr.ecr.us-east-1.amazonaws.com/fbot/downdetector:latest
docker push 240304666027.dkr.ecr.us-east-1.amazonaws.com/fbot/downdetector:latest
aws lambda update-function-code   --function-name fbot-downdetector --image-uri 240304666027.dkr.ecr.us-east-1.amazonaws.com/fbot/downdetector:latest --publish
aws lambda invoke --function-name fbot-downdetector resp.json

