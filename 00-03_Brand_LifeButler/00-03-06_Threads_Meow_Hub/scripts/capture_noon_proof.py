import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

session_path = Path('scripts/threads_session.json')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={'width': 1280, 'height': 1200}, locale='zh-TW')
    page = c.new_page()
    page.goto('https://www.threads.com/@hellotaitung/post/De_DLZekyDD', wait_until='networkidle')
    page.wait_for_timeout(3500)
    proof_path = Path('scripts/screenshots/live_tuesday_noon_proof.png')
    page.screenshot(path=str(proof_path), full_page=True)
    print("Screenshot saved to:", proof_path)
    browser.close()
