@echo off
setlocal
cd /d "%~dp0"
title TRW Workshop WhatsApp Sender

where py >nul 2>&1
if errorlevel 1 (
  echo Python launcher "py" was not found.
  echo Install Python 3.10 or newer and enable the Python Launcher.
  pause
  exit /b 1
)

py -c "import playwright" >nul 2>&1
if errorlevel 1 (
  echo Installing Playwright...
  py -m pip install --upgrade pip
  py -m pip install playwright
  if errorlevel 1 (
    echo Playwright installation failed. Check internet access and try again.
    pause
    exit /b 1
  )
)

echo Installing/checking Playwright Chromium...
py -m playwright install chromium
if errorlevel 1 (
  echo Chromium installation failed. Run: py -m playwright install chromium
  pause
  exit /b 1
)

echo.
echo Starting TRW WhatsApp sender...
py TRW_whatsapp_sender.py
echo.
echo Sender stopped. Review any error above.
pause
