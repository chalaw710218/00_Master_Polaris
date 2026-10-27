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

    # 尋找所有帶有 aria-label 的元素
    for el in page.locator('[aria-label]').all():
        label = el.get_attribute('aria-label')
        if any(w in label for w in ['更多', 'More', '選項', 'Options', '功能表', 'Menu']):
            print("Found candidate menu button:", label, el)
            el.click()
            page.wait_for_timeout(1500)
            break

    page.screenshot(path='scripts/screenshots/post_menu_opened.png')

    for opt in page.locator('div[role="button"], span, div').all():
        t = opt.inner_text().strip()
        if t in ['刪除', 'Delete']:
            print("Found delete option, clicking:", t)
            opt.click()
            page.wait_for_timeout(1500)
            # 確認彈窗
            for c_btn in page.locator('div[role="button"]:has-text("刪除"), button:has-text("刪除")').all():
                if c_btn.is_visible():
                    print("Clicking confirm delete...")
                    c_btn.click()
                    page.wait_for_timeout(3000)
                    break
            break

    page.goto('https://www.threads.com/@hellotaitung/post/De_BWcoE_Xk', wait_until='networkidle')
    page.wait_for_timeout(2000)
    page.screenshot(path='scripts/screenshots/after_delete_check.png')
    print("Page after delete text snippet:", page.inner_text('body')[:200])
    browser.close()
