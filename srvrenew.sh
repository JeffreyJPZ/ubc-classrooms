#!/usr/bin/env bash

# Pulls Certbot image from Docker Hub and renews SSL certs

echo "Beginning renew script"

# Change directory to project root
cd $(dirname "$0")

# Allow use of environment variables from prod.env
source prod.env

# Pull from main branch
sudo git pull origin main && 
echo "Successfully pulled from origin" ||
echo "Error with pulling from origin"

# Login to Docker Hub
echo $DOCKERHUB_TOKEN | sudo docker login -u $DOCKERHUB_USERNAME --password-stdin

# Pull latest Certbot image
sudo docker compose -f compose.srv.yml pull certbot &&
echo "Successfully pulled image" ||
echo "Error with pulling image"

# Remove and renew certs
sudo docker compose -f compose.srv.yml run --rm certbot renew &&
echo "Successfully renewed certs" ||
echo "Error with renewal"

# Reload nginx
sudo docker compose -f compose.srv.yml exec nginx nginx -s reload &&
echo "nginx reloaded" ||
echo "Error with reloading nginx"

echo "Finished"