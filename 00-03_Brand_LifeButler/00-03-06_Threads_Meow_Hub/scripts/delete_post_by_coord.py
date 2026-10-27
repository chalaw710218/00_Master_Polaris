import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

session_path = Path('scripts/threads_session.json')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={'width': 1280, 'height': 1000}, locale='zh-TW')
    page = c.new_page()
    page.goto('https://www.threads.com/@hellotaitung/post/De_BWcoE_Xk', wait_until='networkidle')
    page.wait_for_timeout(2500)

    # 點擊位於 post 內部的三個點按鈕 (坐標大約在 x: 722, y: 114)
    # 尋找所有包含 svg 的按鈕
    buttons = page.locator('div[role="button"]').all()
    target_btn = None
    for b in buttons:
        box = b.bounding_box()
        if box and 700 < box['x'] < 740 and 90 < box['y'] < 140:
            target_btn = b
            print(f"Found target three dots button at {box}")
            break

    if target_btn:
        target_btn.click()
        page.wait_for_timeout(1000)
        page.screenshot(path='scripts/screenshots/dots_clicked.png')
        print("Clicked three dots, looking for 刪除...")
        for opt in page.locator('div[role="menuitem"], div[role="button"], span').all():
            t = opt.inner_text().strip()
            if t == "刪除":
                print("Found '刪除', clicking...")
                opt.click()
                page.wait_for_timeout(1000)
                # 確認對話框
                for confirm in page.locator('button:has-text("刪除"), div[role="button"]:has-text("刪除")').all():
                    if confirm.is_visible():
                        print("Confirming delete...")
                        confirm.click()
                        page.wait_for_timeout(3000)
                        print("🗑️ 成功刪除！")
                        break
                break

    browser.close()
