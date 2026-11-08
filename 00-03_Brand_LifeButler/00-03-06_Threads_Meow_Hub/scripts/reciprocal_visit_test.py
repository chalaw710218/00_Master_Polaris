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
    
    target_user = "oh.ouo"
    print(f"正在登門回訪 @{target_user} 的個人主頁...")
    page.goto(f"https://www.threads.net/@{target_user}", wait_until="domcontentloaded", timeout=25000)
    page.wait_for_timeout(3500)
    
    shot_profile = screenshot_dir / f"profile_{target_user}_visited.png"
    page.screenshot(path=str(shot_profile))
    print(f"📸 主頁截圖已留存: {shot_profile.name}")
    
    # 尋找第一篇貼文或對話
    articles = page.locator('div[data-pressable-container="true"]').all()
    print(f"找到 {len(articles)} 個動態區塊")
    
    found_post = False
    for i, art in enumerate(articles[:3]):
        text = art.inner_text()
        if text and len(text.strip()) > 10:
            print(f"\n📝 貼文 {i+1} 內容摘要:\n{text[:150]}...")
            
            # 嘗試點亮愛心
            like_btn = art.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
            if like_btn.is_visible():
                like_btn.click(force=True)
                page.wait_for_timeout(1000)
                print(f"❤️ 已為 @{target_user} 的最新貼文點亮愛心！")
            
            # 尋找回覆按鈕
            reply_btn = art.locator('div[role="button"]:has(svg[title="Reply"]), div[role="button"]:has(svg[title="回覆"])').first
            if reply_btn.is_visible():
                print(f"💬 找到回覆按鈕，準備登門回訪留言...")
                reply_btn.click(force=True)
                page.wait_for_timeout(1500)
                
                # 輸入框
                input_box = page.locator('div[role="textbox"], textarea, div[contenteditable="true"]').last
                if input_box.is_visible():
                    warm_comment = "生活管家路過串門子～看到你的生活分享特別有意思！週末慢慢過，祝你有個放鬆的好心情🍵✨"
                    input_box.fill(warm_comment)
                    page.wait_for_timeout(1000)
                    
                    shot_typed = screenshot_dir / f"reciprocal_reply_typed_{target_user}.png"
                    page.screenshot(path=str(shot_typed))
                    
                    # 點擊發布按鈕
                    send_btn = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("發布"), button:has-text("發佈"), button:has-text("發布")').last
                    if send_btn.is_visible():
                        send_btn.click(force=True)
                        page.wait_for_timeout(3000)
                        print(f"🎉 成功在 @{target_user} 的最新貼文下留下回訪留言！")
                        shot_done = screenshot_dir / f"reciprocal_reply_done_{target_user}.png"
                        page.screenshot(path=str(shot_done))
                        found_post = True
                        break
            
    if not found_post:
        print(f"ℹ️ @{target_user} 目前主頁可能為非公開、轉發串或無直接可回覆貼文")

    browser.close()
