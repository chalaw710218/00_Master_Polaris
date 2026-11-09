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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    target_url = "https://www.threads.net/@janietaichung/post/Dfe00V8G29Q"
    print(f"前往目標貼文: {target_url}")
    page.goto(target_url, wait_until="networkidle")
    page.wait_for_timeout(4000)
    
    # 點擊對話氣泡以激活輸入框
    bubble = page.locator('div[role="button"]:has(svg[title="回覆"]), svg[title="回覆"]').first
    if bubble.is_visible():
        bubble.click(force=True)
        page.wait_for_timeout(1500)
    
    # 聚焦輸入框
    reply_box = page.locator('div[role="textbox"], div[contenteditable="true"]').first
    if reply_box.is_visible():
        reply_box.click(force=True)
        page.wait_for_timeout(500)
        
        warm_comment = "早安！看你分享的生活步調很舒服～新的一週開工順利，工作忙碌之餘也要記得給自己留一杯茶的休息時間喔！🍵✨"
        page.keyboard.type(warm_comment, delay=25)
        page.wait_for_timeout(1500)
        
        # 尋找圓形發布按鈕
        buttons = page.locator('div[role="button"]').all()
        submit_btn = None
        for b in buttons:
            if b.is_visible():
                box = b.bounding_box()
                if box:
                    if 30 <= box['width'] <= 42 and 30 <= box['height'] <= 42 and 500 <= box['y'] <= 700:
                        print(f"🎯 鎖定發布按鈕: pos=({box['x']}, {box['y']}, w={box['width']}, h={box['height']})")
                        submit_btn = b
                        break
                        
        if submit_btn:
            print("點擊發布按鈕！")
            submit_btn.click(force=True)
        else:
            print("嘗試按 Enter 或點擊座標 (792, 597)...")
            page.mouse.click(792, 597)
            
        page.wait_for_timeout(5000)
        proof = screenshot_dir / "reciprocal_janie_verified.png"
        page.screenshot(path=str(proof))
        print(f"✅ 成功截圖存證: {proof}")
    else:
        print("⚠️ 未找到 reply_box，截圖 debug")
        page.screenshot(path=str(screenshot_dir / "debug_janie.png"))
        
    browser.close()
