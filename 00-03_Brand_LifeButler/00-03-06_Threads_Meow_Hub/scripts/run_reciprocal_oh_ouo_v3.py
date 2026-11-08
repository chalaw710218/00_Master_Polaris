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
    page.wait_for_timeout(4000)
    
    # 點擊對話氣泡以激活輸入框
    bubble = page.locator('div[role="button"]:has(svg[title="回覆"]), svg[title="回覆"]').first
    if bubble.is_visible():
        bubble.click(force=True)
        page.wait_for_timeout(1500)
    
    reply_box = page.locator('div[role="textbox"], div[contenteditable="true"]').first
    reply_box.click(force=True)
    page.wait_for_timeout(500)
    
    warm_comment = "「先做出一個夠爛的原型」——這句話真的直擊靈魂！在台東做生活管家也是這樣，如果等到所有系統都完美才敢出門送第一份菜，很多事情就永遠不會發生了。擁抱粗糙的半成品、親手把泥土摸過一遍，路才會自己長出來。好深刻的分享，默默端上一杯鹿野紅烏龍致敬！🍵✨"
    page.keyboard.type(warm_comment, delay=30)
    page.wait_for_timeout(1500)
    
    # 調查向上箭頭按鈕的屬性
    buttons = page.locator('div[role="button"]').all()
    target_btn = None
    for b in buttons:
        # 檢查是否包含向上箭頭 svg 或 aria-label
        svgs = b.locator('svg').all()
        for s in svgs:
            title = s.get_attribute("title") or ""
            aria = s.get_attribute("aria-label") or ""
            # 印出相關按鈕
            if "發" in title or "發" in aria or "Post" in title or "Post" in aria or not (title or aria):
                pass
    
    # 也可以直接尋找在輸入框旁邊的黑色圓形按鈕（通常帶有特定 role="button" 且位於同一父容器中）
    # 或者用定位：在 contenteditable 祖先容器內的最後一個 role="button"
    # 或者用座標/快捷鍵！
    # 在很多 web app 裡，Ctrl+Enter 或 Cmd+Enter 會觸發發布。
    # 同時，頁面上那個向上箭頭按鈕：
    # 我們可以尋找包含向上箭頭 path 的 svg：
    arrow_btn = page.locator('div[role="button"]:has(svg path[d*="M"]), div[role="button"]:has(svg line)').last
    # 讓我們檢查輸入框容器中的所有按鈕
    container = page.locator('div:has(> div[role="textbox"]), div:has(> div[contenteditable="true"])').first
    container_btns = page.locator('div[role="textbox"] ~ div div[role="button"], div[contenteditable="true"] ~ div div[role="button"]').all()
    print(f"輸入框同層後續按鈕數量: {len(container_btns)}")
    
    # 我們試試快捷鍵 Ctrl+Enter 或者直接點擊最右邊的按鈕
    # 觀察 debug_typed.png，那個黑色圓形按鈕在右側
    # 我們可以用 locator('div[role="button"]').filter(...)
    # 讓我們列出所有可見的無文字 role="button"
    candidates = []
    for b in buttons:
        if b.is_visible():
            txt = b.inner_text().strip()
            box = b.bounding_box()
            if box and not txt:
                # 檢查座標是否在輸入框垂直範圍內 (大約 y 介於 500 ~ 700，x 介於 500 ~ 700)
                if box['y'] > 550 and box['x'] > 550:
                    candidates.append((box, b))
                    print(f"找到候選按鈕: pos=({box['x']}, {box['y']}, w={box['width']}, h={box['height']})")
    
    if candidates:
        # 取最靠右下角的按鈕（即向上箭頭按鈕）
        candidates.sort(key=lambda item: item[0]['x'], reverse=True)
        chosen_box, chosen_btn = candidates[0]
        print(f"選定點擊黑色向上箭頭按鈕: pos=({chosen_box['x']}, {chosen_box['y']})")
        chosen_btn.click(force=True)
        print("已點擊發布箭頭！等待 6 秒...")
        page.wait_for_timeout(6000)
        
        final_proof = screenshot_dir / "reciprocal_oh_ouo_posted_success.png"
        page.screenshot(path=str(final_proof))
        print(f"🎉 截圖驗收: {final_proof.name}")
    else:
        print("未找到候選按鈕，嘗試按鍵 Ctrl+Enter...")
        page.keyboard.press("Control+Enter")
        page.wait_for_timeout(6000)
        page.screenshot(path=str(screenshot_dir / "reciprocal_ctrl_enter.png"))

    browser.close()
