#!/usr/bin/env bash

# Automated data script

echo "Beginning data script..."

# Change directory to project root
cd $(dirname "$0")

# Allow use of environment variables from prod.env
source prod.env

# Start Docker Desktop if using Windows or macOS
if [ "$USER_OS" = "WINDOWS" ] || [ "$USER_OS" = "MACOS" ]; then
    echo "Starting Docker Desktop..."
    ("$PATH_TO_DOCKER_DESKTOP_EXECUTABLE") && 
    echo "Docker Desktop started" || 
    echo "Error with starting Docker Desktop"
fi

# Start Docker daemon if using Linux and it is not running
if [ "$USER_OS" = "LINUX" ] && ! docker info > /dev/null 2>&1; then
  echo "Starting Docker daemon..."
  sudo systemctl start docker &&
  echo "Docker started" ||
  echo "Error with starting Docker"
fi

# Login to Docker Hub
echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin

# Pull images
echo "Pulling Docker images..."
(docker compose -f compose.srv.yml pull scrape-classrooms compute-timeslots) && 
echo "Docker images pulled" || 
echo "Error with pulling Docker images"

# Connect to UBC VPN
echo "Attempting to connect to VPN using credentials..."
(printf "$CWL_USERNAME\n$CWL_PASSWORD\n" | "$PATH_TO_CISCO_ANYCONNECT_EXECUTABLE" -s connect myvpn.ubc.ca) && 
echo "Connected to VPN" || 
echo "Error with connecting to VPN"

# Run script to scrape classrooms
echo "Attempting to scrape UBC Online Timetable..."
(docker compose -f compose.srv.yml run scrape-classrooms) &&
echo "Classrooms successfully scraped" ||
echo "Error with scraping classrooms"

# Disconnect from UBC VPN
echo "Attempting to disconnect from VPN..."
("$PATH_TO_CISCO_ANYCONNECT_EXECUTABLE" disconnect) &&
echo "Disconnected from VPN" ||
echo "Error with disconnecting from VPN"

# Run script to calculate timeslots
echo "Attempting to calculate timeslots"
(docker compose -f compose.srv.yml run compute-timeslots) &&
echo "Timeslots successfully calculated" ||
echo "Error with calculating timeslots"

# Pull changes from main branch
echo "Attempting to pull from origin"
(git pull origin main) && 
echo "Successfully pulled from origin" ||
echo "Error with pulling from origin"

# Add all data to staging area
echo "Attempting to stage data"
(git add backend/data/raw_booking_data backend/data/timeslot_data) &&
echo "Data successfully staged" ||
echo "Error with staging data"

# Commit and push data
echo "Attempting to commit data"
(git commit -m "chore: $(date "+%Y-%m-%d") data bump") &&
echo "Successfully commited" ||
echo "Error with commit"

echo "Attempting to push data"
(git push origin main) &&
echo "Successfully pushed" ||
echo "Error with push"

# Prune dangling images and stopped containers
echo "Attempting to prune unused images and containers"
(echo "y" | docker system prune) && 
echo "Successfully pruned" ||
echo "Error with pruning"

echo "Finished"