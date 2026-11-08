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
    c = browser.new_context(
        storage_state=str(session_path),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = c.new_page()
    
    post_url = "https://www.threads.net/@oh.ouo/post/Dfd67c3DtpP"
    print(f"正在前往貼文: {post_url}")
    page.goto(post_url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # 點擊回覆圖標
    reply_icon = page.locator('svg[title="回覆"], svg[title="Reply"], svg[aria-label="回覆"], svg[aria-label="Reply"]').first
    if reply_icon.is_visible():
        print("點擊回覆圖標以喚起留言框...")
        reply_icon.click(force=True)
        page.wait_for_timeout(2000)
        
        # 尋找彈出框或出現的 textbox
        textbox = page.locator('div[role="textbox"], div[contenteditable="true"]').last
        if textbox.is_visible():
            print("留言輸入框已出現，正在輸入走心回訪留言...")
            textbox.click()
            page.wait_for_timeout(500)
            
            warm_comment = "「先做出一個夠爛的原型」——這句話真的直擊靈魂！在台東做生活管家也是這樣，如果等到所有系統都完美才敢出門送第一份菜，很多事情就永遠不會發生了。擁抱粗糙的半成品、親手把泥土摸過一遍，路才會自己長出來。好深刻的分享，默默端上一杯鹿野紅烏龍致敬！🍵✨"
            page.keyboard.type(warm_comment, delay=25)
            page.wait_for_timeout(1500)
            
            page.screenshot(path=str(screenshot_dir / "reciprocal_typed_proof.png"))
            print("📸 已輸入內容，存證: reciprocal_typed_proof.png")
            
            # 點擊發布按鈕
            post_btn = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("發布"), button:has-text("發佈"), button:has-text("發布")').last
            if post_btn.is_visible():
                print("點擊發布按鈕...")
                post_btn.click(force=True)
                page.wait_for_timeout(4500)
                
                shot_final = screenshot_dir / "reciprocal_posted_proof.png"
                page.screenshot(path=str(shot_final))
                print(f"🎉 登門回訪成功！最新前台存證: {shot_final.name}")
            else:
                print("未找到發布按鈕")
        else:
            print("點擊圖標後未找到輸入框")
    else:
        print("未找到回覆圖標")

    browser.close()
