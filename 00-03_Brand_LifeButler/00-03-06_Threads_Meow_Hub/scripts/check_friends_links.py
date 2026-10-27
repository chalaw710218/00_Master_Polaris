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

    for user in ['sinapayan_youth', 'taitungstation', 'travel_zztaitung', 'hattcoffee']:
        url = f"https://www.threads.com/@{user}"
        page.goto(url, wait_until='networkidle')
        page.wait_for_timeout(2500)
        links = []
        for a in page.locator('a').all():
            href = a.get_attribute('href')
            if href and '/post/' in href:
                if href not in links:
                    links.append(href)
        print(f"User: {user}, links: {links[:3]}")

    browser.close()
