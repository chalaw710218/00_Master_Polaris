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

    # 定位帶有該 3-dots path 的 SVG
    path_loc = page.locator('path[d*="M4 14a2 2 0 1 0 0-4"]')
    print(f"Path matches: {path_loc.count()}")
    if path_loc.count() > 0:
        # 點擊該 path 的父級按鈕
        btn = path_loc.first.locator('xpath=ancestor::div[@role="button"]')
        print("Clicking 3 dots button...")
        btn.click()
        page.wait_for_timeout(1000)
        page.screenshot(path='scripts/screenshots/menu_finally_opened.png')

        # 點擊「刪除」
        del_item = page.locator('div[role="menuitem"]:has-text("刪除"), div[role="button"]:has-text("刪除"), span:has-text("刪除")')
        print(f"Delete item matches: {del_item.count()}")
        if del_item.count() > 0:
            del_item.first.click()
            page.wait_for_timeout(1000)
            page.screenshot(path='scripts/screenshots/confirm_dialog_visible.png')

            # 彈窗確認刪除
            confirm_del = page.locator('div[role="dialog"] div[role="button"]:has-text("刪除"), div[role="dialog"] button:has-text("刪除")')
            print(f"Dialog confirm matches: {confirm_del.count()}")
            if confirm_del.count() > 0:
                confirm_del.last.click()
                page.wait_for_timeout(3000)
                print("🎉 刪除操作已確認！")

    browser.close()
