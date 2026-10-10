@echo off
setlocal
cd /d "%~dp0"
title Build TRW WhatsApp Background EXE

where py >nul 2>&1
if errorlevel 1 (
  echo Python launcher "py" not found. Install Python 3.10+ first.
  pause
  exit /b 1
)

echo Installing build dependencies...
py -m pip install --upgrade pip
py -m pip install playwright pyinstaller
if errorlevel 1 (
  echo Dependency installation failed.
  pause
  exit /b 1
)

echo Installing Playwright Chromium browser...
py -m playwright install chromium
if errorlevel 1 (
  echo Chromium installation failed. Check internet access.
  pause
  exit /b 1
)

echo Building background executable...
py -m PyInstaller --noconfirm --clean --onedir --noconsole ^
  --name TRWWhatsAppBackground ^
  --collect-all playwright ^
  TRW_whatsapp_sender.py

if errorlevel 1 (
  echo.
  echo Build failed. See the error above.
  pause
  exit /b 1
)

echo.
echo BUILD COMPLETE.
echo EXE: dist\TRWWhatsAppBackground\TRWWhatsAppBackground.exe
echo Keep the entire dist\TRWWhatsAppBackground folder together.
echo.
pause
