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

    url = 'https://www.threads.com/@hellotaitung/post/De_BWcoE_Xk'
    print(f"Navigating to {url} to delete...")
    page.goto(url, wait_until='networkidle')
    page.wait_for_timeout(3000)

    # 點擊貼文右上角的三個點（更多選項）
    more_btn = page.locator('svg[aria-label="更多"], svg[aria-label="More"], div[role="button"]:has(svg[aria-label="更多"])').first
    if more_btn.is_visible():
        more_btn.click()
        page.wait_for_timeout(1500)

        # 點擊「刪除」
        del_opt = page.locator('text="刪除", text="Delete"').first
        if del_opt.is_visible():
            del_opt.click()
            page.wait_for_timeout(1500)

            # 確認刪除彈窗
            confirm_del = page.locator('div[role="button"]:has-text("刪除"), button:has-text("刪除")').last
            if confirm_del.is_visible():
                confirm_del.click()
                page.wait_for_timeout(3000)
                print("🗑️ 成功刪除測試貼文！")

    browser.close()
