#!/usr/bin/env bash

# Pulls Certbot image from Docker Hub and renews SSL certs

# Pull from main branch
sudo git pull origin main

# Login to registry
sudo docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN

# Pull latest Certbot image
sudo docker compose -f compose.srv.yml pull certbot

# Remove and renew certs
sudo docker compose -f compose.srv.yml run --rm certbot renew

# Reload nginx
sudo docker compose -f compose.srv.yml exec nginx nginx -s reload