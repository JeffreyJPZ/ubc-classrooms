#!/usr/bin/env bash

# Prod data script
#
# IMPORTANT:
# Replace dependency paths as required with the appropriate OS-specific paths (default is Windows)
# For Windows:
# - Assumes Git Bash is located at default path "C:\Program Files\Git\bin\sh.exe"
# - Assumes Cisco AnyConnect VPN Client CLI is located at default path "C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpncli.exe
# - Assumes Docker Desktop is located at default path "C:\Program Files\Docker\Docker\Docker Desktop.exe"
#
# This script requires a text file named 'vpnconfig.txt' located in the same directory, in the following format:
# --BEGIN--
# connect myvpn.ubc.ca
# <CWL username>
# <CWL password>
# --END--

echo "Beginning setup..."

# Start Docker Desktop
echo "Starting Docker..."
('/c/Program Files/Docker/Docker/Docker Desktop.exe' & wait $!) && 
echo "Docker started" || 
echo "Error with starting Docker"

# Build Docker image
echo "Building Docker image..."
(docker compose -f compose.prod.yml build scrape-classrooms compute-timeslots) && 
echo "Docker image built" || 
echo "Error with building Docker image"

# Connect to UBC VPN, disconnect first
echo "Attempting to connect to VPN using credentials..."
('/c/Program Files (x86)/Cisco/Cisco AnyConnect Secure Mobility Client/vpncli.exe' -s < vpnconfig.txt & wait $!) && 
echo "Connected to VPN" || 
echo "Error with connecting to VPN"

# Run script to scrape classrooms
echo "Attempting to scrape UBC Online Timetable..."
(docker compose -f compose.prod.yml run scrape-classrooms) &&
echo "Classrooms successfully scraped" ||
echo "Error with scraping classrooms"

# Disconnect from UBC VPN
echo "Attempting to disconnect from VPN..."
('/c/Program Files (x86)/Cisco/Cisco AnyConnect Secure Mobility Client/vpncli.exe' disconnect & wait $!)
echo "Disconnected from VPN" ||
echo "Error with disconnecting from VPN"

# Run script to calculate timeslots
echo "Attempting to calculate timeslots"
(docker compose -f compose.prod.yml run compute-timeslots) &&
echo "Timeslots successfully calculated" ||
echo "Error with calculating timeslots"

echo "Finished"