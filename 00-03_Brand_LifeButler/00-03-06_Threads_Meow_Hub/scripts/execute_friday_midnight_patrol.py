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

targets = ["starrytaitung_", "deepcoffee241", "yuan.b778"]
proof_paths = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    
    for target_handle in targets:
        url = f"https://www.threads.net/@{target_handle}"
        print(f"🌌 [週五午夜深夜漫遊] 前往友店: {url}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3500)
            
            # 點亮深夜微光愛心
            like_btn = page.locator('svg[aria-label="讚"], svg[aria-label="Like"]').first
            if like_btn.is_visible(timeout=3000):
                like_btn.click(force=True)
                print(f"  ❤️ 成功為 @{target_handle} 點亮深夜溫暖微光！")
                page.wait_for_timeout(1000)
            else:
                print(f"  ℹ️ @{target_handle} 目前無新貼文或已點選過")
                
            proof = screenshot_dir / f"walk_v3_clout_tea_{target_handle}_friday_midnight.png"
            page.screenshot(path=str(proof))
            print(f"  📸 截圖存證: {proof}")
            proof_paths.append(str(proof))
        except Exception as e:
            print(f"  ⚠️ 造訪 @{target_handle} 異常: {e}")
            
    browser.close()

print(f"🎉 週五午夜友店巡邏拜訪完成，共存檔 {len(proof_paths)} 張實證截圖！")
