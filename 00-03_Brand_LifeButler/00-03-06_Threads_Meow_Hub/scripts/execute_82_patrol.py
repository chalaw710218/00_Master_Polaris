import sys
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
TARGETS_FILE = SCRIPT_DIR / "following_targets.json"

TARGET_USERNAMES = [
    "howhow_sweets",
    "sankou_food_office",
    "yuanlung.667",
    "domine164",
    "yuan.b778",
    "hello_cornerbook",
    "unccoffee",
    "taitungeat"
]

print("==================================================")
print("🎯 [80/20 廣域漏斗社交巡邏啟動]")
print(f"📋 目標名單: {len(TARGET_USERNAMES)} 位在地店家與創作者")
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

            # 尋找第一篇貼文上的愛心按鈕
            like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
            if like_btn.is_visible(timeout=3000):
                like_btn.click(force=True)
                page.wait_for_timeout(1500)
                likes_given += 1
                print(f"  ❤️ 成功為 @{uname} 最新貼文點亮愛心！(累計送出 {likes_given} 顆)")
                results.append({"username": uname, "status": "liked"})
            else:
                print(f"  ℹ️ @{uname} 目前無可點讚之公開動態或按鈕已被點選")
                results.append({"username": uname, "status": "no_button_or_already_liked"})
        except Exception as e:
            print(f"  ⚠️ 訪問 @{uname} 提示: {e}")
            results.append({"username": uname, "status": "error", "error": str(e)})

    browser.close()

print("\n==================================================")
print(f"🎉 [80/20 廣域巡邏完成] 共為 {likes_given} 位在地朋友留下愛心足跡！")
print("==================================================")

with open(SCRIPT_DIR / "latest_82_funnel_result.json", "w", encoding="utf-8") as f:
    json.dump({"timestamp": time.time(), "likes_given": likes_given, "results": results}, f, ensure_ascii=False, indent=2)
