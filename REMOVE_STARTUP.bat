@echo off
setlocal
set "LINK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\TRW WhatsApp Background.lnk"
if exist "%LINK%" (
  del "%LINK%"
  echo Startup launch removed.
) else (
  echo Startup shortcut was not found.
)
pause
