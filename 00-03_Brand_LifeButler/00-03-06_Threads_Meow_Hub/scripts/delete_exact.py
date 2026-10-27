import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

session_path = Path('scripts/threads_session.json')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={'width': 1280, 'height': 1000}, locale='zh-TW')
    page = c.new_page()
    page.goto('https://www.threads.com/@hellotaitung/post/De_BWcoE_Xk', wait_until='networkidle')
    page.wait_for_timeout(3000)

    print("Clicking post three dots at (925, 115)...")
    page.mouse.click(925, 115)
    page.wait_for_timeout(1500)
    page.screenshot(path='scripts/screenshots/menu_at_925_115.png')

    # 點擊「刪除」
    del_btn = page.locator('text="刪除"').first
    if del_btn.is_visible():
        print("Found '刪除', clicking...")
        del_btn.click()
        page.wait_for_timeout(1000)
        confirm_btn = page.locator('div[role="button"]:has-text("刪除"), button:has-text("刪除")').last
        if confirm_btn.is_visible():
            print("Confirming delete...")
            confirm_btn.click()
            page.wait_for_timeout(3000)
            print("🎉 貼文已被徹底刪除！")
    else:
        print("Delete button not found.")

    browser.close()
