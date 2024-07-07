
# Pulls images from Docker Hub and updates database

echo "Beginning db update script"

# Pull from main branch
sudo git pull origin main && 
echo "Successfully pulled from origin" ||
echo "Error with pulling from origin"

# Login to registry
(cat prod.env | grep DOCKERHUB_TOKEN | sed "s/DOCKERHUB_TOKEN=//") | sudo docker login -u ubcclassrooms --password-stdin

# Pull latest images
sudo docker compose -f compose.srv.yml pull create-models delete-expired-timeslots &&
echo "Successfully pulled images" ||
echo "Error with pulling images"

# Add new models
sudo docker compose -f compose.srv.yml run create-models &&
echo "Successfully added models" ||
echo "Error with adding models"

echo "Finished"