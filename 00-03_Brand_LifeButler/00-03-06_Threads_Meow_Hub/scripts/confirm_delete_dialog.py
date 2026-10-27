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

    # 1. 點擊三點按鈕
    page.evaluate('''() => {
        const path = document.elementFromPoint(925, 114);
        const btn = path.closest('div[role="button"]') || path.parentElement;
        btn.click();
    }''')
    page.wait_for_timeout(1000)

    # 2. 點擊刪除
    page.evaluate('''() => {
        const elements = Array.from(document.querySelectorAll('div, span, button'));
        for (const el of elements) {
            if (el.textContent.trim() === '刪除' && el.offsetParent !== null) {
                el.click();
                break;
            }
        }
    }''')
    page.wait_for_timeout(1500)
    page.screenshot(path='scripts/screenshots/confirm_dialog_open.png')

    # 印出所有可見按鈕文字
    buttons = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('button, div[role="button"]'))
            .filter(b => b.offsetParent !== null)
            .map(b => ({
                text: b.textContent.trim(),
                role: b.getAttribute('role'),
                classes: b.className
            }));
    }''')
    print("Visible buttons:", buttons)

    # 點擊最後一個刪除按鈕
    del_btn = page.locator('div[role="dialog"] button, div[role="dialog"] div[role="button"]').all()
    print("Dialog buttons count:", len(del_btn))
    for b in del_btn:
        print("Dialog button text:", b.inner_text().strip())
        if "刪除" in b.inner_text():
            print("Clicking confirmation delete button!")
            b.click()
            page.wait_for_timeout(3000)
            break

    browser.close()
