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
    target_url = "https://www.threads.net/@oh.ouo/post/Dfd67c3DtpP"
    print(f"前往貼文: {target_url}")
    page.goto(target_url, wait_until="networkidle")
    
    # 等待頁面完全加載（骨架屏消失）
    print("等待頁面評論區加載...")
    page.wait_for_timeout(5000)
    
    # 截圖看加載完後的狀態
    page.screenshot(path=str(screenshot_dir / "debug_loaded.png"))
    
    # 尋找含有「回覆oh.ouo」文字或屬性的元素
    reply_box = None
    # 策略 1: 文字匹配
    loc_text = page.locator('text=回覆oh.ouo')
    if loc_text.count() > 0 and loc_text.first.is_visible():
        print("策略 1: 找到包含 '回覆oh.ouo' 文字的元素")
        reply_box = loc_text.first
    else:
        # 策略 2: 尋找 placeholder 或 role="textbox"
        loc_tb = page.locator('div[role="textbox"]')
        if loc_tb.count() > 0 and loc_tb.first.is_visible():
            print("策略 2: 找到 div[role='textbox']")
            reply_box = loc_tb.first
        else:
            # 策略 3: 點擊貼文下方的對話氣泡按鈕
            print("策略 3: 嘗試點擊貼文對話氣泡按鈕...")
            bubble = page.locator('div[role="button"]:has(svg[title="回覆"]), svg[title="回覆"]').first
            if bubble.is_visible():
                bubble.click(force=True)
                page.wait_for_timeout(2000)
                page.screenshot(path=str(screenshot_dir / "debug_after_bubble.png"))
                loc_tb2 = page.locator('div[role="textbox"], div[contenteditable="true"]')
                if loc_tb2.count() > 0:
                    reply_box = loc_tb2.first

    if reply_box:
        print("找到回覆框，點擊聚焦...")
        reply_box.click(force=True)
        page.wait_for_timeout(1000)
        
        warm_comment = "「先做出一個夠爛的原型」——這句話真的直擊靈魂！在台東做生活管家也是這樣，如果等到所有系統都完美才敢出門送第一份菜，很多事情就永遠不會發生了。擁抱粗糙的半成品、親手把泥土摸過一遍，路才會自己長出來。好深刻的分享，默默端上一杯鹿野紅烏龍致敬！🍵✨"
        
        print("正在輸入走心留言...")
        page.keyboard.type(warm_comment, delay=35)
        page.wait_for_timeout(1500)
        
        page.screenshot(path=str(screenshot_dir / "debug_typed.png"))
        print("已截圖輸入狀態: debug_typed.png")
        
        # 尋找發布按鈕
        post_btns = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("發布"), button:has-text("發佈"), button:has-text("發布")').all()
        print(f"找到發布按鈕候選數量: {len(post_btns)}")
        posted = False
        for b in reversed(post_btns):
            if b.is_visible() and b.is_enabled():
                print("點擊發布按鈕！")
                b.click(force=True)
                posted = True
                break
                
        if posted:
            print("已點擊送出，等待 6 秒後台確認...")
            page.wait_for_timeout(6000)
            final_proof = screenshot_dir / "reciprocal_oh_ouo_verified.png"
            page.screenshot(path=str(final_proof))
            print(f"🎉 登門回訪成功發布！最終截圖: {final_proof.name}")
        else:
            print("⚠️ 未找到可點擊的發布按鈕")
    else:
        print("❌ 未能定位到回覆框")

    browser.close()
