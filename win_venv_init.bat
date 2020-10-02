@echo off

echo Creating venv...
py -m venv venv
echo venv created.

echo Activating venv...
call .\venv\Scripts\activate.bat
echo venv activated.

echo Installing packages...
py -m pip install -e .
echo Packages installed.

echo Setting environment variables...

set FLASK_APP=online_dungeons_and_dragons
set FLASK_ENV=development

echo Flask environment variables set.
