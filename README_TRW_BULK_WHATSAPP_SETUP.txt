TRW WORKSHOP — BULK WHATSAPP SETUP (SEAT NUMBER ENABLED)
========================================================

PACKAGE CONTENTS
----------------
TRW_Workshop_Bulk_WhatsApp_SeatNo.html
  Updated workshop website HTML. Adds {{seatNo}} as a WhatsApp message variable and
  exports the seat number in each queue recipient. Default template highlights Seat Number.

TRW_whatsapp_sender.py
  Local visible sender. Watches Windows Downloads for TRW_whatsapp_queue.json,
  opens WhatsApp Web, and processes the queue. If initial navigation gets
  ERR_CONNECTION_RESET, it keeps running and retries every 10 seconds.

START_TRW_WHATSAPP.bat
  Installs Playwright/Chromium if needed and starts the sender.

requirements_TRW_whatsapp.txt
  Python dependency listing.

INSTALLATION
------------
1. Back up your current deployed workshop HTML.
2. Deploy TRW_Workshop_Bulk_WhatsApp_SeatNo.html as your website HTML (rename it to
   index.html if your host requires that filename).
3. Extract this ZIP on the Windows PC that will send messages.
4. Keep TRW_whatsapp_sender.py, START_TRW_WHATSAPP.bat and this README together
   in the same folder.
5. Double-click START_TRW_WHATSAPP.bat.
6. On first run, Playwright and Chromium will be installed. A browser opens.
7. Scan the WhatsApp Web QR code using the WhatsApp account you intend to send from.
   The local session is stored in TRW_WhatsApp_Profile beside the sender script.
8. Keep the sender terminal and browser open.
9. On the website, log in to Admin Dashboard -> Bulk WhatsApp Updates.
10. Select recipients, edit the message, and click Send Updates. The website downloads
    TRW_whatsapp_queue.json to the Windows Downloads folder. The sender detects it.

MESSAGE VARIABLES
-----------------
Use {{seatNo}} to insert the participant's seat number, for example M-001 or F-001.
The default message template now includes:
  Participant Name: {{name}}
  Seat Number: {{seatNo}}

Other supported variables:
  {{name}}, {{registrationNo}}, {{mobile}}, {{gender}}, {{city}}, {{language}}

If a participant has no seat assigned yet, {{seatNo}} is replaced with
"Not assigned yet". Prefer selecting confirmed participants for seat-related notices.
Registration number remains available as an optional variable but is not required.

ERR_CONNECTION_RESET
--------------------
The updated script no longer exits on the initial WhatsApp Web navigation failure;
it retries every 10 seconds. If retries continue:

1. Open https://web.whatsapp.com in ordinary Chrome on the same PC.
2. If it also fails, check internet connection, VPN/proxy, firewall/antivirus, DNS
   filtering, and Windows date/time. Some managed networks block WhatsApp Web.
3. If permitted, test with another trusted network/hotspot.
4. Once normal Chrome can open WhatsApp Web, stop the sender with Ctrl+C and restart it.
5. Reinstalling Playwright will not fix a network reset if the website itself is blocked.

SENDING AND LOGGING
-------------------
- Visible browser; no attempt to bypass WhatsApp security controls.
- Minimum 4-second delay between messages (the script enforces this).
- CSV log: TRW_whatsapp_log.csv beside the sender script.
- Failed recipients are written to Downloads\TRW_whatsapp_failed_queue.json for review.
  Review the log before re-sending; a browser error may occur after a message was sent.
- Pause: create TRW_PAUSE.txt beside the sender script. Delete it to resume.
- "SEND_CLICKED" means the send action was clicked; this does not confirm delivery/read status.
- Use only for relevant workshop updates to participants who agreed to receive them.

LIMITATION
----------
The files' syntax can be checked here, but I cannot sign in to your WhatsApp account
or test a live send from this environment.
