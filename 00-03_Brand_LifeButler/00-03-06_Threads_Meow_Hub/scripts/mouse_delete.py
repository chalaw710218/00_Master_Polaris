import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

session_path = Path('scripts/threads_session.json')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={'width': 1280, 'height': 1000}, locale='zh-TW')
    page = c.new_page()
    page.goto('https://www.threads.com/@hellotaitung/post/De_BWcoE_Xk', wait_until='networkidle')
    page.wait_for_timeout(3000)

    # 直接使用 mouse click
    print("Clicking post three dots at (722, 114)...")
    page.mouse.click(722, 114)
    page.wait_for_timeout(1500)
    page.screenshot(path='scripts/screenshots/after_mouse_click.png')

    # 尋找「刪除」文字
    del_opt = page.locator('text="刪除"').first
    if del_opt.is_visible():
        print("Found 刪除, clicking...")
        del_opt.click()
        page.wait_for_timeout(1000)
        # 確認彈窗內的「刪除」
        confirm_btn = page.locator('div[role="button"]:has-text("刪除"), button:has-text("刪除")').last
        if confirm_btn.is_visible():
            print("Clicking confirm delete...")
            confirm_btn.click()
            page.wait_for_timeout(3000)
            print("🎉 貼文已被徹底刪除！")
    else:
        print("刪除 option not visible after mouse click")

    browser.close()
