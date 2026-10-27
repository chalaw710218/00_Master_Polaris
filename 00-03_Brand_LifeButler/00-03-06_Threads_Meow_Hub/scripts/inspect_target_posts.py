import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

session_path = Path('scripts/threads_session.json')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={'width': 1280, 'height': 1000}, locale='zh-TW')
    page = c.new_page()

    # Taitung Station
    page.goto('https://www.threads.com/@taitungstation/post/DW9A3IICWkx', wait_until='networkidle')
    page.wait_for_timeout(2500)
    print("=== TTSTN Post ===")
    print(page.inner_text('body')[:600])

    # Hatt Coffee new post
    page.goto('https://www.threads.com/@hattcoffee/post/De-2keMCeWh', wait_until='networkidle')
    page.wait_for_timeout(2500)
    print("=== Hatt Coffee New Post ===")
    print(page.inner_text('body')[:600])

    browser.close()
