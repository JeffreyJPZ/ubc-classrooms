@echo off

setlocal
set PATH_TO_GIT_BASH_EXECUTABLE=C:\Program Files\Git\bin\sh.exe
set PATH_TO_SETUP_SCRIPT=./VSCodeProjects/projects/ubc-classrooms/setup.sh

"%PATH_TO_GIT_BASH_EXECUTABLE%" --login -c "%PATH_TO_SETUP_SCRIPT%"

endlocal
