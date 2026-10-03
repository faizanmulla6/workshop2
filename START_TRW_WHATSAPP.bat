@echo off
setlocal
cd /d "%~dp0"
py -c "import playwright" >nul 2>&1
if errorlevel 1 (
  echo Installing Playwright...
  py -m pip install playwright
)
py -m playwright install chromium
py TRW_whatsapp_sender.py
pause
