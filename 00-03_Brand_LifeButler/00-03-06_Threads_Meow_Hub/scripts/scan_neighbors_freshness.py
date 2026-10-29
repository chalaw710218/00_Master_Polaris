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

    for user in ['sinapayan_youth', 'travel_zztaitung', 'taitungstation']:
        url = f'https://www.threads.com/@{user}'
        page.goto(url, wait_until='networkidle')
        page.wait_for_timeout(2500)
        time_el = page.locator('time').first
        time_str = time_el.get_attribute('datetime') if time_el.is_visible() else 'No time'
        first_post = page.locator('a[href*="/post/"]').first
        post_href = first_post.get_attribute('href') if first_post.is_visible() else 'No href'
        print(f"@{user}: latest post = {post_href}, time = {time_str}")

    browser.close()
