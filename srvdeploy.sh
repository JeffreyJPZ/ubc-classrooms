#!/usr/bin/env bash

# Pulls images from Docker Hub and recreates containers

echo "Beginning deploy script"

# Change directory to project root
cd $(dirname "$0")

# Allow use of environment variables from prod.env
source prod.env

# Pull from main branch
sudo git pull origin main && 
echo "Successfully pulled from origin" ||
echo "Error with pulling from origin"

# Login to registry
echo $DOCKERHUB_TOKEN | sudo docker login -u $DOCKERHUB_USERNAME --password-stdin

# Pull latest images
sudo docker compose -f compose.srv.yml pull &&
echo "Successfully pulled image" ||
echo "Error with pulling image"

# Recreate and restart services
sudo docker compose -f compose.srv.yml up db web nginx -d --force-recreate &&
echo "Successfully restarted services" ||
echo "Error with restart"

echo "Finished"