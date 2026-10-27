import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_HUB = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub")
if str(BASE_HUB) not in sys.path:
    sys.path.insert(0, str(BASE_HUB))

from scripts.friend_ledger import record_interaction

SESSION_PATH = BASE_HUB / "scripts" / "threads_session.json"
SCREENSHOT_DIR = BASE_HUB / "scripts" / "screenshots"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    c = browser.new_context(storage_state=str(SESSION_PATH), viewport={'width': 1280, 'height': 1200}, locale='zh-TW')
    page = c.new_page()

    target_user = "hattcoffee"
    target_name = "Hatt Coffee 自家烘焙"
    target_post = "https://www.threads.com/@hattcoffee/post/De-2keMCeWh"

    print(f"Visiting Hatt Coffee new post: {target_post}")
    page.goto(target_post, wait_until='networkidle')
    page.wait_for_timeout(3000)

    # 1. 點讚
    try:
        like_btn = page.locator('svg[aria-label*="讚"]').first
        aria = like_btn.get_attribute("aria-label") or ""
        if "收回讚" not in aria:
            like_btn.click()
            print("❤️ 已點讚主貼文！")
            page.wait_for_timeout(1000)
        else:
            print("❤️ 已經點過讚了。")
    except Exception as e:
        print("Like error:", e)

    # 2. 找到回覆輸入框
    box = page.locator('div[contenteditable="true"]').first
    box_rect = box.bounding_box()
    print("Box rect:", box_rect)
    box.click()
    page.wait_for_timeout(500)

    comment_text = "恭喜海特破 4000 份大關！🎉 4000 份背後代表陪伴了 4000 次溫暖的相聚，真的太不簡單了！本喵已經迫不及待看到一萬份慶祝的那一天，海編跟團隊都辛苦了，繼續加油喵 🥐☕🐾"
    print("Typing comment...")
    page.keyboard.type(comment_text, delay=25)
    page.wait_for_timeout(1000)

    # 3. 點擊送出按鈕 (依據 box 坐標點擊其右側的發佈按鈕)
    clicked = False
    for el in page.locator('div[role="button"], button, svg').all():
        b = el.bounding_box()
        if b and box_rect and abs(b['y'] - box_rect['y']) < 40 and b['x'] > box_rect['x'] + 40:
            print(f"Found submit target at {b}, clicking...")
            el.click(force=True)
            clicked = True
            break

    page.wait_for_timeout(3000)

    # 若打開彈窗，點擊「發佈」
    modal_btn = page.locator('div[role="button"]:has-text("發佈"), button:has-text("發佈")')
    if modal_btn.count() > 0:
        print("Modal opened, clicking 發佈...")
        modal_btn.last.click(force=True)
        page.wait_for_timeout(6000)
    else:
        print("No modal, waiting for direct submit...")
        page.wait_for_timeout(5000)

    # 4. 驗證留言
    page.goto(target_post, wait_until='networkidle')
    page.wait_for_timeout(3000)

    # 點擊 '熱門' 下拉選單切換成 '最新' 以免被熱門演算法折疊
    sort_btn = page.locator('text="熱門"').first
    if sort_btn.is_visible():
        try:
            sort_btn.click()
            page.wait_for_timeout(1000)
            newest_opt = page.locator('text="最新"').first
            if newest_opt.is_visible():
                newest_opt.click()
                page.wait_for_timeout(2000)
        except Exception as e:
            print("Sort toggle note:", e)

    page.evaluate("window.scrollBy(0, 800)")
    page.wait_for_timeout(2000)

    proof_path = SCREENSHOT_DIR / "verified_live_hattcoffee_4000_comment.png"
    page.screenshot(path=str(proof_path), full_page=True)

    text = page.inner_text('body')
    if "恭喜海特破 4000 份大關" in text or "陪伴了 4000 次溫暖的相聚" in text:
        print("🎉 驗證成功！留言已確實出現在 Hatt Coffee 最新貼文留言區！")
        record_interaction(
            username=target_user,
            name=target_name,
            action="like_and_comment",
            post_url=target_post,
            comment_text=comment_text,
            screenshot=str(proof_path)
        )
    else:
        print("⚠️ 頁面未直接檢測到文字，請檢查截圖 verified_live_hattcoffee_4000_comment.png！")

    browser.close()
