TRW WORKSHOP WHATSAPP — BACKGROUND EXE SETUP
=============================================

IMPORTANT
---------
A Windows EXE cannot be compiled reliably for Windows from this hosted Linux environment.
This package includes a Windows build script. Run BUILD_EXE.bat on the Windows PC where
the sender will be used; it builds the EXE locally.

This is a background desktop application, NOT a Windows service. This is intentional:
WhatsApp Web needs a logged-in browser profile and can require QR scanning in the user's
interactive Windows session. Windows services run separately and are not recommended here.

PACKAGE CONTENTS
----------------
- TRW_whatsapp_sender.py: sender with seat-number-aware queue logging and retry behaviour.
- TRW_Workshop_Bulk_WhatsApp_SeatNo.html: website HTML with {{seatNo}} bulk-message variable.
- BUILD_EXE.bat: installs PyInstaller/Playwright and builds the EXE.
- RUN_BACKGROUND.bat: launches the EXE without a console window.
- INSTALL_STARTUP.bat: creates a shortcut in the current Windows user's Startup folder.
- REMOVE_STARTUP.bat: removes that startup shortcut.
- requirements_TRW_background.txt: Python dependency reference.

BUILD ON WINDOWS
----------------
1. Extract this folder to a permanent path, e.g. D:\Workshop registration 2\TRW_WhatsApp_Background_Setup.
2. Ensure Python 3.10+ and the Python Launcher (py) are installed.
3. Double-click BUILD_EXE.bat and allow it to finish.
4. EXE output:
   dist\TRWWhatsAppBackground\TRWWhatsAppBackground.exe
5. Keep the complete dist\TRWWhatsAppBackground folder together. Do not copy only the EXE.
6. Double-click RUN_BACKGROUND.bat, or run the EXE directly.
7. The browser starts minimized. Restore it if WhatsApp Web shows a QR code; scan the QR code.
8. Wait for WhatsApp Web to log in. The profile is stored beside the EXE in TRW_WhatsApp_Profile.
9. The sender watches the current Windows user's Downloads\TRW_whatsapp_queue.json file.
10. In the workshop Admin Dashboard, select participants and click Send Updates.
11. Review TRW_WhatsApp_Background.log and TRW_whatsapp_log.csv when needed.

AUTOMATIC STARTUP
-----------------
After building and testing:
1. Double-click INSTALL_STARTUP.bat.
2. The sender starts automatically when this same Windows user signs in.
3. Windows must be logged in; the PC must be awake and connected to the internet.
4. If the browser needs a fresh login, restore the minimized browser and scan QR.
5. Use REMOVE_STARTUP.bat to disable automatic startup.

SEAT NUMBER TEMPLATE VARIABLE
-----------------------------
Use {{seatNo}} in the Admin Dashboard's bulk WhatsApp message template.
Example:
Participant Name: {{name}}
Seat Number: {{seatNo}}

For participants without a seat number, the website template should handle the missing value
(e.g. "Not assigned yet"). Send seat-number messages only to confirmed participants when possible.

BACKGROUND / SERVICE LIMITATIONS
--------------------------------
- Browser window starts minimized, but may need to be restored for QR login or troubleshooting.
- The PC must be awake and the Windows user must be signed in; sleep/logoff stops processing.
- This package does not bypass WhatsApp controls and cannot guarantee delivery/read status.
- Logs indicate when the sender's Send action was clicked, not confirmed delivery.
- Failed queues should be reviewed carefully before retrying to avoid duplicate messages.
- Use only for relevant workshop updates to recipients who agreed to receive them.

NETWORK ERROR ERR_CONNECTION_RESET
---------------------------------
If the browser cannot open https://web.whatsapp.com, open that URL manually in normal Chrome.
If it also fails there, check internet, VPN/proxy, firewall/antivirus, DNS filtering and system
date/time. The EXE retry loop cannot bypass a network block.

VALIDATION
----------
Python syntax can be checked here, but the Windows EXE must be built on your Windows PC.
Live WhatsApp login and message delivery have not been tested from this environment.
