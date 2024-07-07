# UBC Classrooms

UBC Classrooms is a tool for finding empty classrooms across UBC at specific times. The project uses React, Django and PostgreSQL, with nginx as the web server and Cloudflare as the DNS provider. Deployments are made through GitHub Actions and Docker Hub.

Frontend project structure was inspired by [Bulletproof React](https://github.com/alan2207/bulletproof-react?tab=readme-ov-file#bulletproof-react-%EF%B8%8F-%EF%B8%8F).

## Instructions for running the application locally
1. Ensure that the following dependencies are installed:
   - [Git](https://git-scm.com/downloads)
   - [Node.js v20+](https://nodejs.org/en/download/package-manager)
   - [Cisco AnyConnect Secure Mobility Client](https://www.cisco.com/c/en/us/support/security/anyconnect-secure-mobility-client-v4-x/model.html#~tab-downloads)
   
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
    
3. Create a `dev.env` file in the project's root directory with the following format:

   ```
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DB=ubc_classrooms
   SQL_DB_TEST=ubc_classrooms_test
   SQL_USER=default
   SQL_PASSWORD=default
   SQL_HOST=db
   SQL_PORT=5432
   DB=postgres
   DEBUG=1
   DJANGO_ALLOWED_HOSTS=*
   DJANGO_DEV_SECRET_KEY='django-insecure-$^pvra=ndps97#a#ei#*8(h%_jbs3#&4inla2!(l^x+ry62dat'
   ```
   
4. Create a config file for UBC VPN
   - Follow the instructions in `setup.sh`
      
5. Run the setup script
   - You may have to change some dependency paths depending on your OS — instructions are found in `setup.sh`

   Bash:
   
      ```bash
      $ ./setup.sh
      ```
   
   Windows Command Prompt or Powershell:
   
      ```cmd
      .\setup.bat
      ```
  
7. Start the required services:
   
    ```bash
    $ # Start the web and database services
    $ docker compose -f compose.dev.yml up db web -d --wait
    ```

8. Run the application
   
    ```bash
    $ # Navigate to the UBC Classrooms application
    $ cd frontend
    $ # Install the required dependencies
    $ npm install
    $ # Run the application in development mode
    $ npm run dev
    ```

9. Access the application at http://localhost:3000/

10. To stop the application and reclaim disk space, do the following:
   
    - Press CTRL + C to stop the application and regain control of the command line
    - Run the following commands:
    
      ```bash
      $ # Stops the services
      $ docker -f compose.dev.yml compose down
      $ # Removes services and other utilities, frees up disk space
      $ docker -f compose.dev.yml system prune
      ```
