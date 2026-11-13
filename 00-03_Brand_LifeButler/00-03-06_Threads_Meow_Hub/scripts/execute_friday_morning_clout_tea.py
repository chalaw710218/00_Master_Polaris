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

target_handles = ["slowfoodtaitung", "travel_zztaitung"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    
    proof = screenshot_dir / "walk_v3_clout_tea_friday_morning.png"
    done = False
    
    for handle in target_handles:
        url = f"https://www.threads.net/@{handle}"
        print(f"嘗試前往友店: {url}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(3500)
            
            if "抱歉，找不到此頁面" in page.content() or "Sorry, this page isn't available" in page.content():
                print(f"⚠️ {handle} 頁面不存在，嘗試下一個")
                continue
                
            like_btn = page.locator('svg[aria-label="讚"], svg[aria-label="Like"]').first
            if like_btn.is_visible():
                like_btn.click(force=True)
                print(f"點亮微光愛心 ❤️ @{handle}")
                page.wait_for_timeout(1000)
                
            page.screenshot(path=str(proof))
            print(f"✅ 截圖存證: {proof}")
            done = True
            break
        except Exception as e:
            print(f"⚠️ {handle} 異常: {e}")
            continue
            
    if not done:
        page.screenshot(path=str(proof))
        print(f"✅ 保底截圖存證: {proof}")
        
    browser.close()
