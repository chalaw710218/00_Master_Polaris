#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads Autonomous Walker v3.0 - 週三下午漫遊前哨（訪鄰居、借光端茶與散散步）
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

# 步驟二名單：週三下午茶友店（甜點、咖啡與在地生活）
NEIGHBORS = [
    {"username": "love_love_cat_cake", "name": "小瑪莉貓的手作甜點"},
    {"username": "howhow_sweets", "name": "好好·食甜"},
    {"username": "chaiyuan_bakery", "name": "柴源製菓"},
    {"username": "yuan.b778", "name": "石臼一二"},
    {"username": "unccoffee", "name": "瑰夏咖啡 GESHA COFFEE"},
    {"username": "homu_cafe_", "name": "和暮咖啡"}
]

CLOUT_TEA_TARGET = {
    "username": "love_love_cat_cake",
    "name": "小瑪莉貓的手作甜點",
    "message": "週三下午三點，空氣裡都是小瑪莉家現烤貓咪造型戚風蛋糕的香氣... 生活管家默默在後排端出剛泡好的無糖鹿野紅烏龍，配這塊甜點剛剛好。週三小週末辛苦了，吃塊小蛋糕喝口茶，剩下的半天笑著過！🍵🍰🐱",
    "proof_name": "walk_v3_clout_tea_love_cat_cake_wednesday.png"
}

def run_patrol():
    visited_results = []
    clout_tea_proof = None
    feed_likes = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_PATH),
            viewport={"width": 1280, "height": 900},
            locale="zh-TW"
        )
        page = context.new_page()

        print("\n>>> 步驟二：訪鄰居 (在地友店午後溫暖巡邏) <<<")
        for shop in NEIGHBORS:
            url = f"https://www.threads.net/@{shop['username']}"
            print(f" -> 拜訪 @{shop['username']} ({shop['name']})...")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(3500)

                like_btn = page.locator('svg[aria-label="讚"], svg[aria-label="Like"]').first
                if like_btn.is_visible(timeout=3000):
                    like_btn.click()
                    print(f"   ❤️ 已為 {shop['name']} 最新動態點亮愛心！")
                    visited_results.append({**shop, "action": "liked"})
                    time.sleep(2)
                else:
                    print(f"   ℹ️ {shop['name']} 目前無可點按鈕或已點亮")
                    visited_results.append({**shop, "action": "visited"})
            except Exception as e:
                print(f"   ⚠️ 拜訪 @{shop['username']} 提示: {e}")
                visited_results.append({**shop, "action": "visited"})

        print("\n>>> 步驟二點五：借光端茶協議 (週三下午茶溫暖端茶) <<<")
        clout_url = f"https://www.threads.net/@{CLOUT_TEA_TARGET['username']}"
        shot_clout = SCREENSHOT_DIR / CLOUT_TEA_TARGET["proof_name"]
        try:
            page.goto(clout_url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3500)

            reply_btn = page.locator('svg[aria-label="回覆"], svg[aria-label="Reply"]').first
            if reply_btn.is_visible(timeout=3000):
                reply_btn.click()
                page.wait_for_timeout(1000)
                input_box = page.locator('div[contenteditable="true"], div[role="textbox"]').first
                if input_box.is_visible(timeout=3000):
                    input_box.click()
                    page.keyboard.type(CLOUT_TEA_TARGET["message"], delay=20)
                    page.wait_for_timeout(1000)
                    post_btn = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("Post")').first
                    if post_btn.is_visible(timeout=2000):
                        post_btn.click()
                        page.wait_for_timeout(3000)

            page.screenshot(path=str(shot_clout))
            clout_tea_proof = str(shot_clout)
            print(f"   🍵 借光端茶完成，存證: {shot_clout.name}")
        except Exception as e:
            print(f"   ⚠️ 借光端茶提示: {e}")
            try:
                page.screenshot(path=str(shot_clout))
                clout_tea_proof = str(shot_clout)
            except Exception:
                pass

        print("\n>>> 步驟三：散散步 (首頁為你推薦動態漫遊) <<<")
        try:
            page.goto("https://www.threads.net", wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3500)

            for i in range(4):
                page.mouse.wheel(0, 700)
                page.wait_for_timeout(1500)
                feed_like = page.locator('svg[aria-label="讚"], svg[aria-label="Like"]').nth(i)
                if feed_like.is_visible(timeout=2000):
                    try:
                        feed_like.click()
                        feed_likes += 1
                        print(f"   ❤️ 首頁動態贈送第 {feed_likes}/4 顆午後微光愛心")
                        page.wait_for_timeout(1500)
                    except Exception:
                        pass
        except Exception as e:
            print(f"   ⚠️ 首頁漫步提示: {e}")

        browser.close()

    result_data = {
        "visited_results": visited_results,
        "clout_tea": {
            "target": f"@{CLOUT_TEA_TARGET['username']} ({CLOUT_TEA_TARGET['name']})",
            "message": CLOUT_TEA_TARGET["message"],
            "proof": clout_tea_proof
        },
        "feed_likes": feed_likes
    }

    temp_res = ROOT_DIR / "scripts" / "latest_walk_v3_result.json"
    with open(temp_res, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)

    print("\n🎉 週三下午巡邏前哨成果已沉澱至 latest_walk_v3_result.json")

if __name__ == "__main__":
    run_patrol()
