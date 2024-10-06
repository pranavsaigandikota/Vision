@echo off
title Eye-Controlled Painting Application

REM Navigate to the project directory
cd /d "C:\Users\Pranavsai.Gandikota\Downloads\gazetrack"

REM Activate the virtual environment
call venv\Scripts\activate

REM Run eye_controlled_mouse.py in a new Command Prompt window
start "Eye Control" cmd /k python "0008_USE_EYE_AS_MOUSE_OPENCV\eye_controlled_mouse.py"

REM Run paint.py in another new Command Prompt window
start "Paint Application" cmd /k python "pythonpain\paint.py"

REM Keep the main batch window open until a key is pressed
echo Both scripts are running. Press any key to exit this window.
pause >nul
