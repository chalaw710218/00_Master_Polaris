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

    more_btns = page.locator('svg[aria-label="更多"]')
    print(f"Total '更多' icons: {more_btns.count()}")

    if more_btns.count() >= 2:
        print("Clicking post's more options button (index 1)...")
        more_btns.nth(1).click()
        page.wait_for_timeout(1000)

        # 檢查選單
        for item in page.locator('div[role="menuitem"], div[role="button"], span').all():
            t = item.inner_text().strip()
            if "刪除" in t:
                print(f"🎯 點擊刪除: {t}")
                item.click()
                page.wait_for_timeout(1500)
                # 確認對話框
                confirm = page.locator('button:has-text("刪除"), div[role="button"]:has-text("刪除")')
                if confirm.count() > 0:
                    print("點擊確認刪除...")
                    confirm.last.click()
                    page.wait_for_timeout(3000)
                    print("✅ 貼文刪除成功！")
                break

    browser.close()
