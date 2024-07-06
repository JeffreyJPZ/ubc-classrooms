#!/usr/bin/env bash

# Pulls images from Docker Hub and recreates containers

# Pull from main branch
sudo git pull origin main

# Create production .env file if it doesnt exist already
if [ ! -e "prod.env" ]
then
    sudo touch prod.env
    sudo echo SQL_ENGINE=$SQL_ENGINE >> prod.env
    sudo echo SQL_DB=$SQL_DB >> prod.env
    sudo echo SQL_USER=$SQL_USER >> prod.env
    sudo echo SQL_PASSWORD=$SQL_PASSWORD >> prod.env
    sudo echo SQL_HOST=SQL_HOST >> prod.env
    sudo echo SQL_PORT=$SQL_PORT >> prod.env
    sudo echo DB=$DB >> prod.env
    sudo echo POSTGRES_DB=$POSTGRES_DB >> prod.env
    sudo echo POSTGRES_USER=$POSTGRES_USER >> prod.env
    sudo echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD >> prod.env
    sudo echo DEBUG=$DEBUG >> prod.env
    sudo echo DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS >> prod.env
    sudo echo DJANGO_PROD_SECRET_KEY=$DJANGO_PROD_SECRET_KEY >> prod.env
    sudo echo CERTBOT_EMAIL=$CERTBOT_EMAIL >> prod.env
fi

# Login to registry
sudo docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_TOKEN

# Pull latest images
sudo docker compose -f compose.srv.yml pull

# Recreate and restart services
sudo docker compose -f compose.srv.yml up db web nginx -d --force-recreate