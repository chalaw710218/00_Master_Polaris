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

    # 點擊 closest div[role="button"]
    clicked = page.evaluate('''() => {
        const path = document.elementFromPoint(925, 114);
        if (!path) return "no path";
        const btn = path.closest('div[role="button"]') || path.closest('button') || path.parentElement;
        if (!btn) return "no btn";
        btn.click();
        return "clicked " + btn.tagName;
    }''')
    print("Click result:", clicked)
    page.wait_for_timeout(1500)
    page.screenshot(path='scripts/screenshots/menu_opened_by_closest.png')

    # 尋找刪除按鈕
    del_clicked = page.evaluate('''() => {
        const elements = Array.from(document.querySelectorAll('div, span, button'));
        for (const el of elements) {
            if (el.textContent.trim() === '刪除' && el.offsetParent !== null) {
                el.click();
                return 'clicked delete';
            }
        }
        return 'delete not found';
    }''')
    print("Delete clicked:", del_clicked)
    page.wait_for_timeout(1500)

    # 確認刪除
    confirm_clicked = page.evaluate('''() => {
        const buttons = Array.from(document.querySelectorAll('div[role="button"], button'));
        for (const b of buttons) {
            if (b.textContent.trim() === '刪除' && b.offsetParent !== null) {
                b.click();
                return 'confirmed delete';
            }
        }
        return 'confirm not found';
    }''')
    print("Confirm clicked:", confirm_clicked)
    page.wait_for_timeout(3000)

    browser.close()
