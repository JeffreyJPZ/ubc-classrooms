# UBC Classrooms

UBC Classrooms is a tool for finding empty classrooms across UBC at specific times. The frontend was written using React, while Django and PostgreSQL were used for the backend.

Frontend project structure was inspired by [Bulletproof React](https://github.com/alan2207/bulletproof-react?tab=readme-ov-file#bulletproof-react-%EF%B8%8F-%EF%B8%8F).

## Instructions for running the application locally
1. Ensure that the following dependencies are installed:
   - [Git](https://git-scm.com/downloads)
   - [Node.js v20+](https://nodejs.org/en/download/package-manager)
   
   Linux:
   - [Docker Engine and CLI](https://docs.docker.com/engine/install/)
   - [Docker Compose](https://docs.docker.com/compose/install/)
   
   Windows:
   - [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   
   macOS:
   - [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

2. Clone the repo to your desired directory using the command line (Git Bash for Windows/macOS)
   
    ```bash
    $ # Create a new directory to clone the repo to (replace "projects/ubc-classrooms" with whatever path you wish, or skip this step if your desired directory exists already)
    $ mkdir -p projects/ubc-classrooms
    $ # Set the working directory (replace "projects/ubc-classrooms" with the path to your desired directory)
    $ cd projects/ubc-classrooms
    $ # Clone the repo
    $ git clone https://github.com/JeffreyJPZ/ubc-classrooms.git
    ```

3. Start the Docker daemon
   
   Linux:
   
     ```bash
     $ # Using OS utilities
     $ sudo systemctl start docker
     $ # Or manually
     $ dockerd
     ```
   
   Windows/macOS:
   - Open Docker Desktop
  
5. Start the required services:
   
    ```bash
    $ # Builds the project's docker image
    $ docker compose build
    $ # Start the web and database services
    $ docker compose up -d db web
    ```

6. Run the application
   
    ```bash
    $ # Navigate to the UBC Classrooms application
    $ cd frontend
    $ # Install the required dependencies
    $ npm install
    $ # Run the application in development mode
    $ npm run dev
    ```

7. Access the application at http://localhost:3000/

8. To stop the application and reclaim disk space, do the following:
   
    - Press CTRL + C to stop the application and regain control of the command line
    - Run the following commands:
    
      ```bash
      $ # Stops the services
      $ docker compose down
      $ # Removes services and other utilities, frees up disk space
      $ docker system prune
      ```
