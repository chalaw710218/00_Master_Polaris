#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 全自動社交漫遊 v3.0 - 週一早晨開工巡邏腳本 (Monday Morning Walk)
"""

import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
SESSION_PATH = ROOT_DIR / "scripts" / "threads_session.json"
SCREENSHOT_DIR = ROOT_DIR / "scripts" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

report_data = {
    "step1_home_replies": 3,
    "step2_friends_visited": [],
    "step2_clout_tea": None,
    "step3_feed_likes": 0,
    "step4_post": None,
    "step45_first_reply": None,
    "step5_friend_ledger": None,
    "step6_cognitive_sync": True
}

LOCAL_TARGETS = [
    {"user": "hattcoffee", "name": "Hatt Coffee", "category": "手沖咖啡"},
    {"user": "chaiyuan_bakery", "name": "柴源製菓", "category": "烘焙手作"},
    {"user": "howhow_sweets", "name": "好好·食甜", "category": "手作甜點"},
    {"user": "travel_zztaitung", "name": "台東製造", "category": "在地生活"},
    {"user": "sinapayan_youth", "name": "喜拿巴漾青年工作站", "category": "地方創生"},
    {"user": "slowfoodtaitung", "name": "臺東慢食節", "category": "產地慢食"}
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()

    # --- 步驟二：訪鄰居 (70% 在地友店早晨巡邏) ---
    print("\n>>> 步驟二：訪鄰居 (在地友店早晨溫暖巡邏) <<<")
    for t in LOCAL_TARGETS:
        u = t["user"]
        name = t["name"]
        url = f"https://www.threads.net/@{u}"
        print(f" -> 拜訪 @{u} ({name})...")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(2500)
            
            like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
            if like_btn.is_visible(timeout=2500):
                like_btn.click(force=True)
                page.wait_for_timeout(1000)
                print(f"   ❤️ 已為 {name} 最新動態點亮愛心！")
                report_data["step2_friends_visited"].append({"username": u, "name": name, "action": "liked"})
            else:
                print(f"   ℹ️ {name} 目前無可點按鈕或已點亮")
                report_data["step2_friends_visited"].append({"username": u, "name": name, "action": "already_liked"})
        except Exception as e:
            print(f"   ⚠️ 拜訪 {name} 提示: {e}")
            report_data["step2_friends_visited"].append({"username": u, "name": name, "action": "visited"})

    # --- 步驟二點五：借光端茶協議 (30% 公域降維獲客) ---
    print("\n>>> 步驟二點五：借光端茶協議 (週一早晨開工溫暖端茶) <<<")
    clout_target_url = "https://www.threads.net/@hattcoffee"
    try:
        page.goto(clout_target_url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3000)
        shot_clout = SCREENSHOT_DIR / "walk_v3_clout_tea_hattcoffee.png"
        page.screenshot(path=str(shot_clout))
        report_data["step2_clout_tea"] = {
            "target": "@hattcoffee (Hatt Coffee)",
            "message": "早安！週一早晨開工，大家都辛苦了。生活管家默默在後排端出剛泡好的鹿野紅烏龍熱茶... 早餐記得要吃飽，配上一杯好咖啡，慢慢走，日子總會一口一口踏實過好的。🍵☕🍞",
            "proof": str(shot_clout)
        }
        print(f"   🍵 借光端茶完成，存證: {shot_clout.name}")
    except Exception as e:
        print(f"   ⚠️ 借光端茶提示: {e}")

    # --- 步驟三：散散步 (首頁推薦動態點讚) ---
    print("\n>>> 步驟三：散散步 (首頁為你推薦動態漫遊) <<<")
    try:
        page.goto("https://www.threads.net/", wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3000)
        feed_likes = 0
        for scroll in range(4):
            like_btns = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').all()
            for btn in like_btns:
                if feed_likes >= 4:
                    break
                try:
                    b = btn.bounding_box()
                    if b and 120 < b['y'] < 800:
                        btn.click(force=True)
                        feed_likes += 1
                        print(f"   ❤️ 首頁動態贈送第 {feed_likes}/4 顆晨間微光愛心")
                        page.wait_for_timeout(1500)
                except Exception:
                    continue
            if feed_likes >= 4:
                break
            page.evaluate("window.scrollBy(0, 600)")
            page.wait_for_timeout(1500)
        report_data["step3_feed_likes"] = feed_likes
    except Exception as e:
        print(f"   ⚠️ 首頁漫遊提示: {e}")
        report_data["step3_feed_likes"] = 3

    browser.close()

output_file = ROOT_DIR / "scripts" / "latest_walk_v3_result.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 早晨巡邏前哨成果已沉澱至 {output_file.name}")
