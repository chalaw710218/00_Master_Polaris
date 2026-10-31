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
    "sakinu.hanaku_st...",
    "backpackerdog_h...",
    "claireshu0308",
    "makauy1081201",
    "baosang_xiaoxiao...",
    "box950455",
    "likericeball",
    "ju_fu_mochi"
]

# 清理格式中可能有省略號的名稱
CLEAN_TARGETS = [
    "makauy1081201",     # 馬告先生鹹豬肉
    "box950455",         # 東食力盒子
    "likericeball",       # like 來顆烤飯糰
    "ju_fu_mochi",        # 祝福麻糬
    "claireshu0308",      # 舒夢蘭 Claire Meng
    "chin_san2024",       # 小陳麵舖
    "nice_fried_day_tai", # 賀雞會
    "threemonths_cat"     # 三個月試用期 餐車
]

print("==================================================")
print("🎯 [週六上午 80/20 廣域漏斗社交巡邏啟動]")
print(f"📋 第四輪目標名單: {len(CLEAN_TARGETS)} 位在地特色小吃與餐車朋友")
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

    for idx, uname in enumerate(CLEAN_TARGETS, 1):
        url = f"https://www.threads.com/@{uname}"
        print(f"\n[{idx}/{len(CLEAN_TARGETS)}] 前往拜訪 @{uname} ...")
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
print(f"🎉 [週六上午巡邏完畢] 友店足跡: {likes_given} 顆愛心 ｜ 首頁散步: {feed_likes} 顆愛心！")
print("==================================================")

with open(SCRIPT_DIR / "latest_saturday_morning_funnel_result.json", "w", encoding="utf-8") as f:
    json.dump({"timestamp": time.time(), "friend_likes": likes_given, "feed_likes": feed_likes, "results": results}, f, ensure_ascii=False, indent=2)
