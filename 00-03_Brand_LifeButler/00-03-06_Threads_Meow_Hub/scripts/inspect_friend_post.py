import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(SESSION_PATH), viewport={"width": 1280, "height": 900})
    page = c.new_page()
    page.goto('https://www.threads.com/@hattcoffee/post/DfJL5UNCaB5', wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)
    
    # 取出所有可見文字
    body_text = page.locator('main').inner_text()
    print("PAGE MAIN TEXT:")
    print(body_text)
    page.screenshot(path=str(SCRIPT_DIR / "hattcoffee_post.png"))
    browser.close()
