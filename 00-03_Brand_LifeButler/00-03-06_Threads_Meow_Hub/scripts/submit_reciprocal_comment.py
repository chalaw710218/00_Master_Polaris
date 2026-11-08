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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    page.goto("https://www.threads.net/@oh.ouo/post/Dfd67c3DtpP", wait_until="networkidle")
    page.wait_for_timeout(2500)
    
    # 點擊回覆圖標
    btn = page.locator('div[role="button"]:has(svg[title="回覆"]), div[role="button"]:has(svg[title="Reply"])').first
    if btn.is_visible():
        btn.click(force=True)
        print("已點擊回覆按鈕，等待彈窗與輸入框就緒...")
        
        # 等待輸入框就緒並點擊
        tb = page.wait_for_selector('div[role="textbox"]', timeout=8000)
        tb.click()
        page.wait_for_timeout(800)
        
        warm_comment = "「先做出一個夠爛的原型」——這句話真的直擊靈魂！在台東做生活管家也是這樣，如果等到所有系統都完美才敢出門送第一份菜，很多事情就永遠不會發生了。擁抱粗糙的半成品、親手把泥土摸過一遍，路才會自己長出來。好深刻的分享，默默端上一杯鹿野紅烏龍致敬！🍵✨"
        page.keyboard.type(warm_comment, delay=25)
        page.wait_for_timeout(1500)
        
        shot_typed = screenshot_dir / "reciprocal_typed_oh_ouo.png"
        page.screenshot(path=str(shot_typed))
        print(f"📸 輸入完成存證: {shot_typed.name}")
        
        # 尋找發布按鈕
        post_btn = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("發布"), button:has-text("發佈"), button:has-text("發布")').last
        post_btn.click(force=True)
        page.wait_for_timeout(5000)
        
        shot_final = screenshot_dir / "reciprocal_posted_oh_ouo_success.png"
        page.screenshot(path=str(shot_final))
        print(f"🎉 登門回訪成功！前台驗收存證: {shot_final.name}")
    else:
        print("未找到回覆按鈕")

    browser.close()
