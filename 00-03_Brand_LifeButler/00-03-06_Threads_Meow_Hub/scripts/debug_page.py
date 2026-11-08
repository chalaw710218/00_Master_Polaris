import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

session_path = Path("scripts/threads_session.json")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    page.goto("https://www.threads.net/@oh.ouo/post/Dfd67c3DtpP", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    page.screenshot(path="scripts/screenshots/debug_oh_ouo_post.png")
    print("Title:", page.title())
    print("URL:", page.url)
    
    # 找找是否有回覆按鈕
    reply_icons = page.locator('svg[title="回覆"], svg[title="Reply"], svg[aria-label="回覆"], svg[aria-label="Reply"]').all()
    print(f"找到 {len(reply_icons)} 個回覆圖標")
    
    # 找文字包含「回覆」或「說點什麼」
    placeholders = page.locator('text="回覆", text="說點什麼", text="Reply"').all()
    print(f"找到 {len(placeholders)} 個回覆文字區域")
    for ph in placeholders[:5]:
        print(" - Placeholder text:", ph.inner_text())

    browser.close()
