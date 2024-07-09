
# Pulls images from Docker Hub and updates database

echo "Beginning db update script"

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

# Pull latest images
sudo docker compose -f compose.srv.yml pull create-models delete-expired-timeslots &&
echo "Successfully pulled images" ||
echo "Error with pulling images"

# Add new models
sudo docker compose -f compose.srv.yml run create-models &&
echo "Successfully added models" ||
echo "Error with adding models"

# Recreate and restart services
sudo docker compose -f compose.srv.yml up db web nginx -d --force-recreate &&
echo "Successfully restarted services" ||
echo "Error with restart"

echo "Finished"