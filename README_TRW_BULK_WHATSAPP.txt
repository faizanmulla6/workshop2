TRW BULK WHATSAPP SENDER v3

This version uses a different sending approach:
- It opens each WhatsApp chat without putting the message in the URL.
- It explicitly targets the WhatsApp Web message composer inside the chat footer.
- It types the message into the composer.
- It clicks the visible Send button when available, otherwise presses Enter.
- It keeps Chrome visible and uses a persistent local browser profile.

SETUP
1. Install Python 3.10+.
2. Double-click START_TRW_WHATSAPP.bat.
3. If prompted, the script installs Playwright and Chromium/Chrome dependencies.
4. Scan WhatsApp Web QR once.
5. Keep the sender window open.
6. In the workshop Admin Dashboard select participants and click Send Updates.

IMPORTANT
- Do not close the sender window while a queue is being processed.
- WhatsApp Web must remain logged in.
- Keep the delay at a reasonable value. The script enforces a minimum of 4 seconds.
- TRW_PAUSE.txt beside the Python script pauses sending; delete it to resume.
- A CSV log is written beside the script.


UPDATED v4 FEATURES
-------------------
Admin Dashboard -> Bulk WhatsApp Updates now includes:
- Status filter: All / Confirmed / Pending / Cancelled
- Gender filter: All / Male / Female
- Language filter: All / Urdu / Hindi / English
- Delay: 2 to 10 seconds
- Individual participant checkboxes
- Select all visible
- Clear selection
- Clear filters
- Selected recipient count
- Estimated sending time in Preview Count
- Gender-wise summary: Male/Female Confirmed and Pending
- Existing search, message variables, pause/resume and CSV sending log are retained.

IMPORTANT:
The 2-10 second delay is configurable as requested. The sender remains visible and rate-limited.
