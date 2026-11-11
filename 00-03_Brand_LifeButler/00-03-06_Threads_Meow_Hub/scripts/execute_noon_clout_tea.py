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

target_handle = "slowfoodtaitung"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    url = f"https://www.threads.net/@{target_handle}"
    print(f"前往友店: {url}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3500)
        
        # 點讚最新一篇
        like_btn = page.locator('svg[aria-label="讚"], svg[aria-label="Like"]').first
        if like_btn.is_visible():
            like_btn.click(force=True)
            print("點亮微光愛心 ❤️")
            page.wait_for_timeout(1000)
            
        proof = screenshot_dir / "walk_v3_clout_tea_slowfoodtaitung_tuesday_noon.png"
        page.screenshot(path=str(proof))
        print(f"✅ 截圖存證: {proof}")
    except Exception as e:
        print(f"⚠️ 異常: {e}")
    finally:
        browser.close()
