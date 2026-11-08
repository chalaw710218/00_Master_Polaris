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
    print(f"導航至: {target_url}")
    page.goto(target_url, wait_until="networkidle")
    page.wait_for_timeout(3000)
    
    # 找到回覆按鈕
    # 注意：Threads 貼文主體下方的回覆按鈕通常帶有 svg title="回覆" 或 aria-label="回覆"
    reply_triggers = page.locator('div[role="button"]:has(svg[title="回覆"]), div[role="button"]:has(svg[aria-label="回覆"]), svg[title="回覆"]').all()
    print(f"找到回覆觸發元素數量: {len(reply_triggers)}")
    
    if reply_triggers:
        reply_triggers[0].click(force=True)
        print("已點擊第一個回覆觸發元素，等待 2.5 秒...")
        page.wait_for_timeout(2500)
    
    page.screenshot(path=str(screenshot_dir / "step1_after_trigger.png"))
    
    # 尋找可編輯的輸入框
    # 嘗試多種可能選擇器
    candidates = [
        'div[contenteditable="true"]',
        'div[role="textbox"]',
        'p[data-placeholder]',
        'textarea'
    ]
    
    target_input = None
    for cand in candidates:
        loc = page.locator(cand)
        count = loc.count()
        print(f"選擇器 '{cand}' 匹配數: {count}")
        if count > 0:
            for idx in range(count):
                elem = loc.nth(idx)
                if elem.is_visible():
                    print(f"  -> 找到可見輸入框 [{idx}] 來自 {cand}!")
                    target_input = elem
                    break
        if target_input:
            break
            
    if target_input:
        print("點擊聚焦輸入框...")
        target_input.click()
        page.wait_for_timeout(500)
        
        warm_comment = "「先做出一個夠爛的原型」——這句話真的直擊靈魂！在台東做生活管家也是這樣，如果等到所有系統都完美才敢出門送第一份菜，很多事情就永遠不會發生了。擁抱粗糙的半成品、親手把泥土摸過一遍，路才會自己長出來。好深刻的分享，默默端上一杯鹿野紅烏龍致敬！🍵✨"
        
        print(f"正在輸入走心留言...")
        page.keyboard.type(warm_comment, delay=30)
        page.wait_for_timeout(1500)
        
        page.screenshot(path=str(screenshot_dir / "step2_typed.png"))
        print("已截圖: step2_typed.png")
        
        # 尋找發布按鈕
        # 在 Modal 或輸入框下方，通常有文字為「發布」或「發佈」的按鈕
        post_btns = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("發布"), button:has-text("發佈"), button:has-text("發布")').all()
        print(f"找到發布按鈕數量: {len(post_btns)}")
        
        posted = False
        for b in reversed(post_btns):
            if b.is_visible():
                print("點擊發布按鈕！")
                b.click(force=True)
                posted = True
                break
                
        if posted:
            print("已送出，等待 5 秒後台處理與頁面響應...")
            page.wait_for_timeout(5000)
            page.screenshot(path=str(screenshot_dir / "step3_posted_verified.png"))
            print("🎉 驗收截圖完成: step3_posted_verified.png")
        else:
            print("⚠️ 未找到可點擊的發布按鈕")
    else:
        print("❌ 仍未找到任何輸入框")

    browser.close()
