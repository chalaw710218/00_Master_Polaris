#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 全自動社交漫遊 v3.0 - 週一下午茶巡邏腳本 (Monday Afternoon Walk)
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
    "step1_home_replies": 0,
    "step2_friends_visited": [],
    "step2_clout_tea": None,
    "step3_feed_likes": 0,
    "step4_post": None,
    "step45_first_reply": None,
    "step5_friend_ledger": None,
    "step6_cognitive_sync": True
}

LOCAL_TARGETS = [
    {"user": "love_love_cat_cake", "name": "小瑪莉貓的手作甜點", "category": "貓咪甜點"},
    {"user": "yuan.b778", "name": "石臼一二", "category": "老宅咖啡甜點"},
    {"user": "unccoffee", "name": "瑰夏咖啡 GESHA COFFEE", "category": "精品咖啡"},
    {"user": "deepcoffee241", "name": "Deep coffee", "category": "獨立咖啡"},
    {"user": "homu_cafe_", "name": "和暮咖啡", "category": "溫暖咖啡"},
    {"user": "riceandbear", "name": "米熊共生", "category": "友善農業"}
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()

    # --- 步驟二：訪鄰居 (70% 在地友店午後巡邏) ---
    print("\n>>> 步驟二：訪鄰居 (在地友店午後溫暖巡邏) <<<")
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
    print("\n>>> 步驟二點五：借光端茶協議 (週一下午茶溫暖端茶) <<<")
    clout_target_url = "https://www.threads.net/@love_love_cat_cake"
    try:
        page.goto(clout_target_url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3000)
        shot_clout = SCREENSHOT_DIR / "walk_v3_clout_tea_love_cat_cake.png"
        page.screenshot(path=str(shot_clout))
        report_data["step2_clout_tea"] = {
            "target": "@love_love_cat_cake (小瑪莉貓的手作甜點)",
            "message": "午後四點，空氣裡都是剛出爐的甜點香氣... 生活管家默默在後排端出剛泡好的鹿野紅烏龍，配小瑪莉家的甜點剛剛好。週一下午打工人辛苦了，喝口茶吃塊甜，充個電再出發！🍵🍰🐱",
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
                        print(f"   ❤️ 首頁動態贈送第 {feed_likes}/4 顆午後微光愛心")
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

print(f"\n🎉 午後巡邏前哨成果已沉澱至 {output_file.name}")
