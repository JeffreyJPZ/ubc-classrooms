#!/usr/bin/env bash

# Setup script
#
# IMPORTANT:
# Replace dependency paths as required with the appropriate OS-specific paths (default is Windows)
# For Windows:
# - Assumes Git Bash is located at default path "C:\Program Files\Git\bin\sh.exe"
# - Assumes Cisco AnyConnect VPN Client CLI is located at default path "C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpncli.exe
# - Assumes Docker Desktop is located at default path "C:\Program Files\Docker\Docker\Docker Desktop.exe"
#
# This script requires a text file named 'vpnconfig.txt' located in the same directory, in the following format:
# connect myvpn.ubc.ca
# <CWL username>
# <CWL password>

echo "Beginning setup script"

# Change directory to project root
cd $(dirname "$0")

# Allow use of environment variables from prod.env
source prod.env

# Start Docker Desktop if using Windows or macOS
if [ "$USER_OS" = "WINDOWS" ] || [ "$USER_OS" = "MACOS" ]; then
    echo "Starting Docker..."
    "$PATH_TO_DOCKER_DESKTOP_EXECUTABLE" && 
    echo "Docker started" || 
    echo "Error with starting Docker"
fi

# Start Docker daemon if using Linux and it is not running
if [ "$USER_OS" = "LINUX" ] && ! docker info > /dev/null 2>&1; then
  echo "Starting Docker daemon..."
  sudo systemctl start docker &&
  echo "Docker started" ||
  echo "Error with starting Docker"
fi

# Build Docker image
echo "Building Docker image..."
(docker compose -f compose.dev.yml build) && 
echo "Docker image built" || 
echo "Error with building Docker image"

# Connect to UBC VPN, disconnect first
echo "Attempting to connect to VPN using credentials..."
(printf "$CWL_USERNAME\n$CWL_PASSWORD\n" | "$PATH_TO_CISCO_ANYCONNECT_EXECUTABLE" -s connect myvpn.ubc.ca) && 
echo "Connected to VPN" || 
echo "Error with connecting to VPN"

# Run script to scrape classrooms
echo "Attempting to scrape UBC Online Timetable..."
(docker compose -f compose.dev.yml run scrape-classrooms) &&
echo "Classrooms successfully scraped" ||
echo "Error with scraping classrooms"

# Disconnect from UBC VPN
echo "Attempting to disconnect from VPN..."
("$PATH_TO_CISCO_ANYCONNECT_EXECUTABLE" disconnect)
echo "Disconnected from VPN" ||
echo "Error with disconnecting from VPN"

# Run script to calculate timeslots
echo "Attempting to calculate timeslots"
(docker compose -f compose.dev.yml run compute-timeslots) &&
echo "Timeslots successfully calculated" ||
echo "Error with calculating timeslots"

# Run script to populate db with timeslots
echo "Attempting to create timeslots in db"
(docker compose -f compose.dev.yml run create-models) &&
echo "Timeslots successfully created" ||
echo "Error with creating timeslots"

# Run script to remove expired timeslots
echo "Attempting to remove expired timeslots"
(docker compose -f compose.dev.yml run delete-expired-timeslots) &&
echo "Expired timeslots successfully deleted" ||
echo "Error with deleting expired timeslots"

echo "Finished"