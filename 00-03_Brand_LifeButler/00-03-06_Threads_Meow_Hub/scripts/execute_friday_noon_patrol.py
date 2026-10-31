import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"

TARGET_USERNAMES = [
    "threedays_2019",
    "bagel.chasing",
    "shuramen.taitung",
    "taikkacp_hang_bah",
    "tsao_min",
    "wowspangcah",
    "ms.ricewine",
    "taitunghouse"
]

print("==================================================")
print("🎯 [週五午後 80/20 廣域漏斗社交巡邏啟動]")
print(f"📋 全新第三輪目標名單: {len(TARGET_USERNAMES)} 位在地獨立名店與文化社群")
print("==================================================")

likes_given = 0
results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 850},
        locale="zh-TW"
    )
    page = context.new_page()

    for idx, uname in enumerate(TARGET_USERNAMES, 1):
        url = f"https://www.threads.com/@{uname}"
        print(f"\n[{idx}/{len(TARGET_USERNAMES)}] 前往拜訪 @{uname} ...")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3000)

            like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
            if like_btn.is_visible(timeout=3000):
                like_btn.click(force=True)
                page.wait_for_timeout(1500)
                likes_given += 1
                print(f"  ❤️ 成功為 @{uname} 最新動態點亮愛心！(累計送出 {likes_given} 顆)")
                results.append({"username": uname, "status": "liked"})
            else:
                print(f"  ℹ️ @{uname} 目前無可點讚之動態或按鈕已點選")
                results.append({"username": uname, "status": "no_button_or_already_liked"})
        except Exception as e:
            print(f"  ⚠️ 訪問 @{uname} 提示: {e}")
            results.append({"username": uname, "status": "error", "error": str(e)})

    # 散散步：首頁海巡點讚 2 篇
    print("\n🌐 進入首頁推薦動態牆散散步...")
    feed_likes = 0
    try:
        page.goto("https://www.threads.com/", wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3000)
        for _ in range(3):
            page.mouse.wheel(0, 600)
            page.wait_for_timeout(2000)
            feed_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
            if feed_btn.is_visible(timeout=2000):
                feed_btn.click(force=True)
                feed_likes += 1
                print(f"  ❤️ 首頁推薦送出第 {feed_likes} 顆愛心！")
                page.wait_for_timeout(2000)
                if feed_likes >= 2:
                    break
    except Exception as e:
        print("首頁散步提示:", e)

    browser.close()

print("\n==================================================")
print(f"🎉 [午後巡邏完畢] 友店足跡: {likes_given} 顆愛心 ｜ 首頁散步: {feed_likes} 顆愛心！")
print("==================================================")

with open(SCRIPT_DIR / "latest_friday_noon_funnel_result.json", "w", encoding="utf-8") as f:
    json.dump({"timestamp": time.time(), "friend_likes": likes_given, "feed_likes": feed_likes, "results": results}, f, ensure_ascii=False, indent=2)
