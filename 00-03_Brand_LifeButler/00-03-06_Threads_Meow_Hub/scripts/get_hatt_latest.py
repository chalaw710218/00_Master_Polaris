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
    page.goto('https://www.threads.net/@hattcoffee', wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)
    
    # 找第一篇貼文的連結與文字
    post_link = page.locator('a[href*="/post/"]').first
    url = post_link.get_attribute("href") if post_link.is_visible() else "None"
    
    # 抓取第一篇貼文的文字區塊
    article = page.locator('div[data-pressable-container="true"]').first
    text = article.inner_text() if article.is_visible() else "None"
    
    print("Post URL:", url)
    print("Post Text:")
    print(text)
    
    browser.close()
