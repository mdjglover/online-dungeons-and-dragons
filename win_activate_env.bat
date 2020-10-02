@echo off
echo Activating venv...
call .\venv\Scripts\activate.bat
echo Setting environment variables...

set FLASK_APP=online_dungeons_and_dragons
set FLASK_ENV=development

echo Flask environment variables set.