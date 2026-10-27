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

    # 拜訪 sinapayan 喜拿巴漾青年工作站
    target_user = "sinapayan_youth"
    target_name = "喜拿巴漾青年工作站"
    profile_url = f"https://www.threads.com/@{target_user}"
    print(f"Visiting {profile_url}...")
    page.goto(profile_url, wait_until='networkidle')
    page.wait_for_timeout(3000)

    # 抓取第一篇可訪問的貼文
    post_links = page.locator('a[href*="/post/"]').all()
    target_post = None
    for link in post_links:
        href = link.get_attribute('href')
        if href and "/post/" in href:
            if not href.startswith("http"):
                href = "https://www.threads.com" + href
            target_post = href
            break

    print("Found target post:", target_post)
    if not target_post:
        # 備用：若喜拿巴漾無貼文，轉訪台東站 taitungstation
        print("No post found for sinapayan_youth, trying taitungstation...")
        target_user = "taitungstation"
        target_name = "台東站 TTSTN"
        page.goto(f"https://www.threads.com/@{target_user}", wait_until='networkidle')
        page.wait_for_timeout(3000)
        post_links = page.locator('a[href*="/post/"]').all()
        for link in post_links:
            href = link.get_attribute('href')
            if href and "/post/" in href:
                if not href.startswith("http"):
                    href = "https://www.threads.com" + href
                target_post = href
                break

    if target_post:
        print(f"Navigating to post: {target_post}")
        page.goto(target_post, wait_until='networkidle')
        page.wait_for_timeout(3000)

        # 1. 點讚主貼文
        try:
            like_btn = page.locator('svg[aria-label*="讚"]').first
            if like_btn.is_visible() and "收回讚" not in (like_btn.get_attribute("aria-label") or ""):
                like_btn.click()
                print("❤️ 已點讚主貼文！")
                page.wait_for_timeout(1000)
        except Exception as e:
            print("Like note:", e)

        # 2. 點擊輸入框
        box = page.locator('div[contenteditable="true"]').first
        if not box.is_visible():
            page.evaluate("window.scrollBy(0, 300)")
            page.wait_for_timeout(1000)
            box = page.locator('div[contenteditable="true"]').first

        box.click()
        page.wait_for_timeout(500)

        comment_text = "看到在地青年聚在一起為土地做事的能量真的很棒！中午大太陽辛苦了，喵編路過送上一顆大大的愛心應援喵 🌾☀️🐾"
        print("Typing comment:", comment_text)
        page.keyboard.type(comment_text, delay=20)
        page.wait_for_timeout(1000)

        # 3. 點擊送出按鈕 (依據 box 坐標點擊或尋找按鈕)
        box_rect = box.bounding_box()
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
            print("Waiting for direct submit...")
            page.wait_for_timeout(5000)

        # 重新整理驗證
        page.goto(target_post, wait_until='networkidle')
        page.wait_for_timeout(4000)
        page.evaluate("window.scrollBy(0, 500)")
        page.wait_for_timeout(2000)

        proof_path = SCREENSHOT_DIR / f"verified_live_{target_user}_comment.png"
        page.screenshot(path=str(proof_path), full_page=True)

        text = page.inner_text('body')
        if "在地青年聚在一起" in text:
            print(f"🎉 驗證成功！留言已確實出現在 {target_name} 貼文下方！")
            record_interaction(
                username=target_user,
                name=target_name,
                action="like_and_comment",
                post_url=target_post,
                comment_text=comment_text,
                screenshot=str(proof_path)
            )
        else:
            print(f"⚠️ 提示：未在頁面文字中匹配到留言，請檢查截圖！")

    browser.close()
