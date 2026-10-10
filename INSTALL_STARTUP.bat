@echo off
setlocal
cd /d "%~dp0"
set "EXE=%~dp0dist\TRWWhatsAppBackground\TRWWhatsAppBackground.exe"
if not exist "%EXE%" (
  echo EXE not found. Run BUILD_EXE.bat first.
  pause
  exit /b 1
)
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup\TRW WhatsApp Background.lnk')); $s.TargetPath='%EXE%'; $s.WorkingDirectory='%~dp0dist\TRWWhatsAppBackground'; $s.WindowStyle=7; $s.Description='TRW workshop WhatsApp queue sender'; $s.Save()"
if errorlevel 1 (
  echo Could not create Startup shortcut.
  pause
  exit /b 1
)
echo Installed. TRW WhatsApp Background will start when you sign in to Windows.
echo This is a per-user startup app, not a Windows service.
pause
