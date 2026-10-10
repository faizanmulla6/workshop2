@echo off
setlocal
cd /d "%~dp0"
set "EXE=%~dp0dist\TRWWhatsAppBackground\TRWWhatsAppBackground.exe"
if not exist "%EXE%" (
  echo EXE not found. Run BUILD_EXE.bat first.
  pause
  exit /b 1
)
start "" "%EXE%"
echo Background sender launched. Check TRW_WhatsApp_Background.log beside the EXE if troubleshooting is needed.
