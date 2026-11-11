import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

session_path = Path("scripts/threads_session.json")
screenshot_dir = Path("scripts/screenshots")
screenshot_dir.mkdir(parents=True, exist_ok=True)

url = "https://www.threads.com/@hellotaitung/post/DfjpUHSGvJ-"
proof = screenshot_dir / "walk_v3_reply_brush_teeth_verified.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    print(f"前往貼文截圖留言: {url}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(4000)
        page.screenshot(path=str(proof))
        print(f"✅ 截圖存證: {proof}")
    except Exception as e:
        print(f"⚠️ 異常: {e}")
    finally:
        browser.close()
