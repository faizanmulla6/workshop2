#!/usr/bin/env python3
"""
TRW WhatsApp Web Sender

How it works:
1. Keep this program running.
2. Log in to WhatsApp Web in the browser window it opens (scan QR once).
3. In the workshop Admin Dashboard click "Send All Updates".
4. The downloaded TRW_whatsapp_queue.json is detected automatically.
5. Messages are opened and sent one-by-one with a configurable delay.

This is intentionally a visible, rate-limited sender. Pause by creating a file
named TRW_PAUSE.txt beside this script; delete it to resume.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
except ImportError:
    print("Playwright is not installed. Run:")
    print("  py -m pip install playwright")
    print("  py -m playwright install chromium")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
DOWNLOADS = Path.home() / "Downloads"
QUEUE_NAME = "TRW_whatsapp_queue.json"
QUEUE = DOWNLOADS / QUEUE_NAME
ARCHIVE = DOWNLOADS / "TRW_whatsapp_archive"
PROFILE = BASE_DIR / "TRW_WhatsApp_Profile"
PAUSE_FILE = BASE_DIR / "TRW_PAUSE.txt"
LOG_FILE = BASE_DIR / "TRW_whatsapp_log.csv"

# Use installed Chrome when available; otherwise Playwright Chromium.
CHROME_CANDIDATES = [
    Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Google/Chrome/Application/chrome.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")) / "Google/Chrome/Application/chrome.exe",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe",
]
CHROME = next((p for p in CHROME_CANDIDATES if p.exists()), None)


def log_line(reg, mobile, status, detail="", seat_no=""):
    import csv
    first = not LOG_FILE.exists()
    with LOG_FILE.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if first:
            writer.writerow(["timestamp", "registration", "seat_no", "mobile", "status", "detail"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), reg, seat_no, mobile, status, detail])


def wait_if_paused():
    if PAUSE_FILE.exists():
        print("\n⏸ PAUSED — delete TRW_PAUSE.txt to continue.")
        while PAUSE_FILE.exists():
            time.sleep(1)
        print("▶ Resuming...")


def load_queue():
    if not QUEUE.exists():
        return None
    try:
        data = json.loads(QUEUE.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("recipients"), list):
            raise ValueError("Invalid queue format")
        return data
    except Exception as e:
        print(f"⚠ Cannot read queue: {e}")
        return None


def archive_queue():
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = ARCHIVE / f"TRW_whatsapp_queue_{stamp}.json"
    try:
        shutil.move(str(QUEUE), str(dest))
        return dest
    except Exception as e:
        print("Could not archive queue:", e)
        return None


def send_one(page, mobile, message):
    url = "https://web.whatsapp.com/send?phone=91" + mobile
    detail = ""
    for attempt in range(1, 4):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            composer = page.locator('footer div[contenteditable="true"][role="textbox"]').last
            composer.wait_for(state="visible", timeout=60000)
            composer.click()
            composer.fill(message)
            time.sleep(0.8)
            send_btn = page.locator('button[aria-label="Send"]:visible').last
            if send_btn.count() > 0:
                send_btn.click()
            else:
                composer.press("Enter")
            time.sleep(2)
            return True, "send action clicked; delivery is not verified"
        except PlaywrightTimeoutError:
            detail = "chat/composer timed out; verify WhatsApp Web login and recipient number"
        except PlaywrightError as exc:
            detail = str(exc).replace("\\n", " ")[:220]
        except Exception as exc:
            detail = str(exc).replace("\\n", " ")[:220]
        print(f"    ⚠ attempt {attempt}/3 failed: {detail}")
        if attempt < 3:
            time.sleep(10)
    return False, detail


def send_queue(page, data):
    recipients = data.get("recipients", [])
    try:
        requested_delay = int(data.get("delaySeconds", 8))
    except (TypeError, ValueError):
        requested_delay = 8
    delay = min(30, max(4, requested_delay))
    total = len(recipients)
    print(f"\\n📲 Queue received: {total} message(s). Delay: {delay}s")
    failed = []

    for idx, r in enumerate(recipients, 1):
        wait_if_paused()
        mobile = ''.join(c for c in str(r.get("mobile", "")) if c.isdigit())[-10:]
        reg = str(r.get("registrationNo", ""))
        seat = str(r.get("seatNo", ""))
        name = str(r.get("name", ""))
        message = str(r.get("message", ""))

        if len(mobile) != 10 or mobile[0] not in "6789":
            print(f"[{idx}/{total}] SKIP {seat or reg} {name}: invalid mobile")
            log_line(reg, mobile, "SKIPPED", "invalid mobile", seat)
            continue
        if not message.strip():
            print(f"[{idx}/{total}] SKIP {seat or reg} {name}: empty message")
            log_line(reg, mobile, "SKIPPED", "empty message", seat)
            continue

        print(f"[{idx}/{total}] Sending → {seat or reg or 'Participant'} | {name} | {mobile}")
        ok, detail = send_one(page, mobile, message)
        if ok:
            print("    ✓ send action clicked (check WhatsApp for delivery)")
            log_line(reg, mobile, "SEND_CLICKED", detail, seat)
        else:
            print("    ✗ failed:", detail)
            log_line(reg, mobile, "FAILED", detail, seat)
            failed.append(r)

        if idx < total:
            for _ in range(delay):
                wait_if_paused()
                time.sleep(1)

    archived = archive_queue()
    print("\\nQueue processing finished.")
    if archived:
        print("Archived:", archived)
    print("Log:", LOG_FILE)
    if failed:
        retry_path = DOWNLOADS / "TRW_whatsapp_failed_queue.json"
        retry_path.write_text(json.dumps({
            "version": data.get("version", 1),
            "createdAt": datetime.now().isoformat(),
            "delaySeconds": delay,
            "workshop": data.get("workshop", ""),
            "recipients": failed,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{len(failed)} failed item(s) saved for review: {retry_path}")
        print("Review the log before retrying; do not resend messages that may already have delivered.")


def main():
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    print("=" * 64)
    print("TRW Workshop WhatsApp Web Sender")
    print("=" * 64)
    print("Queue file:", QUEUE)
    print("Browser profile:", PROFILE)
    print("Pause file:", PAUSE_FILE)
    print("Sending log:", LOG_FILE)
    print("\nKeep this window and its browser open. Use only for relevant updates to participants who agreed to receive them.")
    print("Minimum delay between messages: 4 seconds.")

    with sync_playwright() as pw:
        launch_kwargs = dict(
            user_data_dir=str(PROFILE),
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--start-maximized"],
        )
        if CHROME:
            launch_kwargs["executable_path"] = str(CHROME)
            print("Using Chrome:", CHROME)
        else:
            print("Installed Chrome not found; using Playwright Chromium.")

        context = pw.chromium.launch_persistent_context(**launch_kwargs)
        try:
            page = context.pages[0] if context.pages else context.new_page()
            attempt = 0
            while True:
                attempt += 1
                print(f"\nOpening WhatsApp Web (attempt {attempt})...")
                try:
                    page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded", timeout=60000)
                    print("WhatsApp Web page loaded.")
                    break
                except (PlaywrightTimeoutError, PlaywrightError) as exc:
                    print("Could not connect to WhatsApp Web:", str(exc).replace("\n", " ")[:220])
                    print("Check if https://web.whatsapp.com opens in normal Chrome; check internet, VPN/proxy, firewall, DNS filtering, and system date/time.")
                    print("Retrying in 10 seconds; the sender will remain open.")
                    time.sleep(10)

            print("\n1) If QR code appears, scan it with your phone.")
            print("2) Wait until WhatsApp Web is logged in.")
            print("3) In the workshop Admin Dashboard, open Bulk WhatsApp Updates and click Send Updates.")
            print("4) The queue JSON in Downloads will be detected automatically.\n")

            while True:
                if QUEUE.exists():
                    data = load_queue()
                    if data is not None:
                        send_queue(page, data)
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nStopped by user. Browser profile is preserved.")
        finally:
            context.close()


if __name__ == "__main__":
    main()
