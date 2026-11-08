import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

session_path = Path("scripts/threads_session.json")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = c.new_page()
    page.goto("https://www.threads.net/@oh.ouo/post/Dfd67c3DtpP", wait_until="networkidle")
    page.wait_for_timeout(2500)
    
    # 點擊回覆
    btn = page.locator('div[role="button"]:has(svg[title="回覆"]), div[role="button"]:has(svg[title="Reply"])').first
    if btn.is_visible():
        btn.click(force=True)
        page.wait_for_timeout(2000)
        page.screenshot(path="scripts/screenshots/after_click_reply_oh_ouo.png")
        print("截圖已留存: after_click_reply_oh_ouo.png")
        
        # 尋找所有輸入元素
        inputs = page.locator('input, textarea, [contenteditable="true"], [role="textbox"]').all()
        print(f"找到輸入元素數量: {len(inputs)}")
        for i, inp in enumerate(inputs):
            tag = inp.evaluate("el => el.tagName")
            role = inp.get_attribute("role")
            placeholder = inp.get_attribute("placeholder") or inp.get_attribute("aria-placeholder")
            print(f" - [{i}] Tag: {tag}, Role: {role}, Placeholder: {placeholder}")
    else:
        print("未找到回覆按鈕")

    browser.close()
