@echo off
SETLOCAL

REM ————————————————————————————————————————————————
REM 1) Install Python silently if needed
REM ————————————————————————————————————————————————
REM The Python installer lives in the “Python installer” subfolder
set "PY_INSTALLER=%~dp0Python installer\python-3.13.5-amd64.exe"

if exist "%PY_INSTALLER%" (
  echo Installing Python…
  "%PY_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
) else (
  echo Python installer not found at "%PY_INSTALLER%". Skipping.
)

REM ————————————————————————————————————————————————
REM 2) Set up user‐writable app directory and venv
REM ————————————————————————————————————————————————
set "TARGET_DIR=%LOCALAPPDATA%\TheBrainMQTTAuto"
set "VENV_DIR=%TARGET_DIR%\venv"

echo Copying application files to %TARGET_DIR%…
mkdir "%TARGET_DIR%" 2>nul
xcopy /y /e /i "%~dp0The_Brain_MQTT_AUTO.py"        "%TARGET_DIR%\" >nul
xcopy /y /e /i "%~dp0memory.txt"                     "%TARGET_DIR%\" >nul
xcopy /y /e /i "%~dp0APIKEY.txt"                     "%TARGET_DIR%\" >nul
xcopy /y /e /i "%~dp0mqtt_credentials.txt"           "%TARGET_DIR%\" >nul
xcopy /y /e /i "%~dp0templates"                      "%TARGET_DIR%\templates"  >nul
xcopy /y /e /i "%~dp0static"                         "%TARGET_DIR%\static"     >nul

if not exist "%VENV_DIR%" (
  echo Creating virtual environment…
  python -m venv "%VENV_DIR%"
)

echo Activating venv and installing dependencies…
call "%VENV_DIR%\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install flask flask-socketio eventlet paho-mqtt google-generativeai

echo.
echo ** Setup complete **
echo To run the app:
echo   cd /d "%TARGET_DIR%"
echo   call venv\Scripts\activate.bat
echo   python The_Brain_MQTT_AUTO.py
pause
ENDLOCAL
