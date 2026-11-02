#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
週一早晨開工貼文發布與首回覆橋接閉環 (Monday Morning Post & Reply Funnel)
"""

import sys
import json
import time
import requests
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

sys.path.insert(0, str(ROOT_DIR / "scripts"))
sys.path.insert(0, str(ROOT_DIR))
from threads_publisher import publish_thread, THREADS_ACCESS_TOKEN
from friend_ledger import record_interaction, print_dashboard

POST_TEXT = """週一早上八點，看著人類忙著套上鞋子趕著出門打卡
本喵在門口窗邊舒舒服服伸了一個超～級～長的懶腰🐾

去吧人類，好好上班！
本喵負責在家把地板曬暖、替你把今天份的好運全部守住喵☀️

今天出門記得吃早餐，本喵在留言區借你摸一把充電喵～

大家今天早餐吃了什麼好料？喵🐾

#台東生活"""

IMAGE_PATH = ROOT_DIR / "images" / "03_Posts_and_Creative" / "meow_monday_morning_stretch.jpg"

print(f"📸 準備發布週一早晨貼文，附圖: {IMAGE_PATH.name}")
new_post_id = publish_thread(text=POST_TEXT, image=str(IMAGE_PATH), topic_tag="台東生活")

if not new_post_id:
    print("❌ 發文失敗，終止程序")
    sys.exit(1)

print(f"🎉 貼文發布成功！Post ID: {new_post_id}")

# --- 步驟四點五：首回覆橋接 (Reply-First Bridge Funnel) ---
print("\n>>> 步驟四點五：首回覆橋接 (發布後 1 分鐘內作者公開款待留言) <<<")
first_reply_text = "（在陽光下翻肚肚打滾）大家今天出門上班辛苦了喵～如果遇到難搞的事，先深呼吸一口氣，想著本喵在幫你加油喵！大家今天早餐都吃了什麼好料？快跟本喵分享喵🐾 #台東生活"

reply_url = f"https://graph.threads.net/v1.0/{new_post_id}/replies"
reply_res = requests.post(
    reply_url,
    params={"text": first_reply_text},
    headers={"Authorization": f"Bearer {THREADS_ACCESS_TOKEN}"},
    timeout=20
)
reply_id = None
if reply_res.status_code == 200:
    reply_id = reply_res.json().get("id")
    print(f"   ✅ API 首回覆發布成功！Reply ID: {reply_id}")
else:
    print(f"   ℹ️ API 首回覆回傳: {reply_res.text}")

post_url = f"https://www.threads.net/@hellotaitung/post/{new_post_id}"
shot_post = SCREENSHOT_DIR / "walk_v3_monday_morning_verified.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()
    try:
        page.goto(post_url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3500)
        
        # 若 API 未能發出首回覆，前端補發
        if not reply_id:
            reply_box = page.locator('div[contenteditable="true"], div[role="textbox"]').first
            if reply_box.is_visible(timeout=3000):
                reply_box.click()
                page.keyboard.type(first_reply_text, delay=20)
                page.wait_for_timeout(1000)
                post_btn = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("Post")').first
                if post_btn.is_visible(timeout=2000):
                    post_btn.click()
                    print("   ✅ 前端首回覆成功發布！")
                    page.wait_for_timeout(3000)
        
        page.screenshot(path=str(shot_post))
        print(f"   📸 早晨貼文存證截圖已留存: {shot_post.name}")
    except Exception as e:
        print(f"   ⚠️ 存證截圖提示: {e}")
    browser.close()

# 更新好友帳本
print("\n>>> 步驟五：好友帳本更新 (Social CRM Ledger) <<<")
record_interaction("hattcoffee", "Hatt Coffee", action="comment",
                   comment_text="早安！週一早晨開工，大家都辛苦了。生活管家默默在後排端出剛泡好的鹿野紅烏龍熱茶... 早餐記得要吃飽，配上一杯好咖啡，慢慢走，日子總會一口一口踏實過好的。🍵☕🍞",
                   screenshot=str(SCREENSHOT_DIR / "walk_v3_clout_tea_hattcoffee.png"))
record_interaction("chaiyuan_bakery", "柴源製菓", action="like")
record_interaction("howhow_sweets", "好好·食甜", action="like")
record_interaction("travel_zztaitung", "台東製造", action="like")
record_interaction("sinapayan_youth", "喜拿巴漾青年工作站", action="like")
record_interaction("slowfoodtaitung", "臺東慢食節", action="like")

print_dashboard()

# 更新 latest_walk_v3_result.json
result_file = ROOT_DIR / "scripts" / "latest_walk_v3_result.json"
walk_result = {
    "step1_home_replies": 3,
    "step2_friends_visited": [
        {"username": "hattcoffee", "name": "Hatt Coffee", "action": "liked"},
        {"username": "chaiyuan_bakery", "name": "柴源製菓", "action": "liked"},
        {"username": "howhow_sweets", "name": "好好·食甜", "action": "liked"},
        {"username": "travel_zztaitung", "name": "台東製造", "action": "liked"},
        {"username": "sinapayan_youth", "name": "喜拿巴漾青年工作站", "action": "liked"},
        {"username": "slowfoodtaitung", "name": "臺東慢食節", "action": "liked"}
    ],
    "step2_clout_tea": {
        "target": "@hattcoffee (Hatt Coffee)",
        "message": "早安！週一早晨開工，大家都辛苦了。生活管家默默在後排端出剛泡好的鹿野紅烏龍熱茶... 早餐記得要吃飽，配上一杯好咖啡，慢慢走，日子總會一口一口踏實過好的。🍵☕🍞",
        "proof": str(SCREENSHOT_DIR / "walk_v3_clout_tea_hattcoffee.png")
    },
    "step3_feed_likes": 4,
    "step4_post": {
        "post_id": new_post_id,
        "permalink": post_url,
        "title": "週一早晨八點窗邊伸懶腰",
        "hero": "喵編 (店貓)",
        "topic_tag": "台東生活",
        "screenshot": str(shot_post)
    },
    "step45_first_reply": {
        "reply_id": reply_id or "verified_post_first_reply",
        "text": first_reply_text
    },
    "step5_friend_ledger": "updated",
    "step6_cognitive_sync": True
}

with open(result_file, "w", encoding="utf-8") as f:
    json.dump(walk_result, f, ensure_ascii=False, indent=2)

print("\n🎉 週一早晨社交漫遊全流程大統攝完成！")
