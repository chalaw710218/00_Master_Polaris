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

target_handle = "travel_zztaitung"
comment = "週一早晨看著台東的藍天與山景，真的會讓人瞬間忘記開工焦慮。生活管家默默在後排端出剛泡好的鹿野紅烏龍熱茶～祝所有在台東打拼的大家，新的一週都從從容容、元氣滿滿！🍵✨"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    url = f"https://www.threads.net/@{target_handle}"
    print(f"前往友店: {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=25000)
    page.wait_for_timeout(3500)
    
    # 點讚最新一篇
    like_btn = page.locator('svg[aria-label="讚"], svg[aria-label="Like"]').first
    if like_btn.is_visible():
        like_btn.click(force=True)
        print("點亮微光愛心 ❤️")
        page.wait_for_timeout(1000)
        
    proof = screenshot_dir / "walk_v3_clout_tea_travel_zztaitung.png"
    page.screenshot(path=str(proof))
    print(f"✅ 截圖存證: {proof}")
    browser.close()
