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

    page.goto('https://www.threads.com/@hattcoffee/post/De-2keMCeWh', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # 檢查所有包含 "回覆" 的元素或 svg
    print("Looking for reply triggers...")
    reply_elements = page.locator('text*="回覆"').all()
    for el in reply_elements:
        print("Text:", el.inner_text(), "Tag:", el.evaluate("el => el.tagName"), "Visible:", el.is_visible())

    # 檢查 svg aria-label
    for svg in page.locator('svg').all():
        aria = svg.get_attribute('aria-label')
        if aria and ('回覆' in aria or '留言' in aria or '讚' in aria):
            print("SVG aria:", aria)

    browser.close()
