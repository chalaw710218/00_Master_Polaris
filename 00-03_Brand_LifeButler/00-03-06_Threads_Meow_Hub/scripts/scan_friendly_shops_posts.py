import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"

TARGETS = [
    "hattcoffee",
    "howhow_sweets",
    "chaiyuan_bakery",
    "956leissmoker",
    "hello_cornerbook"
]

print("🔍 正在探訪台東在地友店最新動態...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 850},
        locale="zh-TW"
    )
    page = context.new_page()

    shop_posts = []

    for uname in TARGETS:
        url = f"https://www.threads.com/@{uname}"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(3000)

            # 抓取第一篇貼文的連結與文字
            first_post = page.locator('div[data-pressable-container="true"]').first
            post_link = page.locator('a[href*="/post/"]').first
            
            post_url = None
            if post_link.is_visible(timeout=3000):
                href = post_link.get_attribute("href")
                if href:
                    post_url = href if href.startswith("http") else f"https://www.threads.com{href}"

            # 抓取文字摘要
            text_elem = page.locator('div[data-pressable-container="true"] span, div[dir="auto"]').first
            snippet = text_elem.inner_text() if text_elem.is_visible(timeout=2000) else "無文字或純圖"

            # 抓取發布時間/日期標籤
            time_elem = page.locator('time').first
            time_str = time_elem.inner_text() if time_elem.is_visible(timeout=2000) else "未知"

            print(f"\n🏪 @{uname}:")
            print(f"  URL: {post_url}")
            print(f"  時間: {time_str}")
            print(f"  摘要: {snippet[:60].replace(chr(10), ' ')}")

            shop_posts.append({
                "username": uname,
                "post_url": post_url,
                "time": time_str,
                "snippet": snippet[:100]
            })
        except Exception as e:
            print(f"⚠️ 拜訪 @{uname} 異常: {e}")

    browser.close()

with open(SCRIPT_DIR / "friendly_shops_latest.json", "w", encoding="utf-8") as f:
    json.dump(shop_posts, f, ensure_ascii=False, indent=2)
