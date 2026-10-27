import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

session_path = Path('scripts/threads_session.json')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(session_path), viewport={'width': 1280, 'height': 1200}, locale='zh-TW')
    page = c.new_page()

    url = 'https://www.threads.com/@hellotaitung/replies'
    print(f"Navigating to {url}...")
    page.goto(url, wait_until='networkidle')
    page.wait_for_timeout(3000)
    page.screenshot(path='scripts/screenshots/my_replies_tab.png')

    # 檢查是否有小八貓
    print("Found 小八貓 in replies?", "小八貓" in page.inner_text('body'))

    # 定位該留言旁的 3-dots 按鈕
    hachi_loc = page.locator('div:has-text("小八貓跟吉伊卡哇")').last
    if hachi_loc.is_visible():
        rect = hachi_loc.bounding_box()
        print("Reply rect:", rect)
        # 尋找鄰近的 3-dots 按鈕 (y 差在 60px 以內)
        clicked = page.evaluate('''y => {
            const svgs = Array.from(document.querySelectorAll('svg'));
            for (const s of svgs) {
                const label = s.getAttribute('aria-label') || s.getAttribute('title') || '';
                const r = s.getBoundingClientRect();
                if ((label.includes('更多') || label.includes('More')) && Math.abs(r.y - y) < 80) {
                    const btn = s.closest('div[role="button"]') || s.parentElement;
                    btn.click();
                    return { clicked: true, x: r.x, y: r.y };
                }
            }
            return { clicked: false };
        }''', rect['y'])
        print("Clicked more button:", clicked)
        page.wait_for_timeout(1000)
        page.screenshot(path='scripts/screenshots/my_reply_menu.png')

        # 點擊「刪除」
        del_clicked = page.evaluate('''() => {
            const items = Array.from(document.querySelectorAll('div, span, button'));
            for (const it of items) {
                if (it.textContent.trim() === '刪除' && it.offsetParent !== null) {
                    it.click();
                    return true;
                }
            }
            return false;
        }''')
        print("Delete clicked:", del_clicked)
        page.wait_for_timeout(1000)

        # 確認刪除
        confirm_clicked = page.evaluate('''() => {
            const items = Array.from(document.querySelectorAll('div[role="dialog"] div[role="button"], div[role="dialog"] button'));
            for (const it of items) {
                if (it.textContent.trim() === '刪除' && it.offsetParent !== null) {
                    it.click();
                    return true;
                }
            }
            return false;
        }''')
        print("Confirm clicked:", confirm_clicked)
        page.wait_for_timeout(3000)

    # 重新整理驗證
    page.goto(url, wait_until='networkidle')
    page.wait_for_timeout(2500)
    print("Is 小八貓 still present?", "小八貓" in page.inner_text('body'))

    browser.close()
