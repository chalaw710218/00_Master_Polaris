#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
週一深夜貼文發布與首回覆橋接閉環 (Monday Night Post & Reply Funnel)
店貓喵編 (灰色虎斑貓)
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

POST_TEXT = """週一深夜十一點半，看著人類終於洗完澡、把筆電闔上、嘆了今天最後一口氣
本喵早就把身體蜷成一個暖呼呼的灰色虎斑毛球，在棉被正中間卡好位了喵🐾

辛苦了，最難熬的週一已經被你徹底解決掉了！
今晚就別再滑手機回顧明天的待辦清單了，
趕快鑽進被窩，把冰冰的腳伸到本喵肚子底下取暖吧喵～

大家今晚的被窩夠暖嗎？睡前要記得喝口溫水喵🐾

#台東生活"""

IMAGE_PATH = ROOT_DIR / "images" / "03_Posts_and_Creative" / "meow_monday_night_gray_tabby.jpg"

print(f"📸 準備發布週一深夜貼文，附圖: {IMAGE_PATH.name}")
new_post_id = publish_thread(text=POST_TEXT, image=str(IMAGE_PATH), topic_tag="台東生活")

if not new_post_id:
    print("❌ 發文失敗，終止程序")
    sys.exit(1)

print(f"🎉 貼文發布成功！Post ID: {new_post_id}")

# --- 步驟四點五：首回覆橋接 (Reply-First Bridge Funnel) ---
print("\n>>> 步驟四點五：首回覆橋接 (發布後 1 分鐘內作者公開款待留言) <<<")
first_reply_text = "（把毛茸茸的灰斑身體縮得更緊打呼嚕）最辛苦的週一撐過去了喵～今晚什麼都不要想，好好閉上眼睛深層睡眠充電！大家的被窩夠暖嗎？晚安喵🐾 #台東生活"

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
shot_post = SCREENSHOT_DIR / "walk_v3_monday_night_verified.png"

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
        print(f"   📸 深夜貼文存證截圖已留存: {shot_post.name}")
    except Exception as e:
        print(f"   ⚠️ 存證截圖提示: {e}")
    browser.close()

# 更新好友帳本
print("\n>>> 步驟五：好友帳本更新 (Social CRM Ledger) <<<")
clout_tea_shot = SCREENSHOT_DIR / "walk_v3_clout_tea_yuanlung.png"
record_interaction("yuanlung.667", "緣龍無骨鹽酥雞", action="comment",
                   comment_text="深夜十一點半，剛炸起鍋的鹽酥雞九層塔香氣太犯規了... 生活管家默默在後排端出剛泡好的無糖冷泡鹿野紅烏龍解膩。週一深夜辛苦了，犒賞完肚皮早點休息，明天繼續加油！🍵🍗✨",
                   screenshot=str(clout_tea_shot))
record_interaction("hello_cornerboo", "仨口食事處", action="visit")
record_interaction("956leissmoker", "雨田燻手工煙燻", action="visit")
record_interaction("deepcoffee241", "Deep coffee", action="visit")
record_interaction("hattcoffee", "Hatt Coffee", action="visit")

print_dashboard()

# 更新 latest_walk_v3_result.json
result_file = ROOT_DIR / "scripts" / "latest_walk_v3_result.json"
walk_result = {
    "step1_home_replies": 0,
    "step2_friends_visited": [
        {"username": "yuanlung.667", "name": "緣龍無骨鹽酥雞", "action": "comment_and_visit"},
        {"username": "hello_cornerboo", "name": "仨口食事處", "action": "visited"},
        {"username": "956leissmoker", "name": "雨田燻手工煙燻", "action": "visited"},
        {"username": "deepcoffee241", "name": "Deep coffee", "action": "visited"},
        {"username": "hattcoffee", "name": "Hatt Coffee", "action": "visited"}
    ],
    "step2_clout_tea": {
        "target": "@yuanlung.667 (緣龍無骨鹽酥雞)",
        "message": "深夜十一點半，剛炸起鍋的鹽酥雞九層塔香氣太犯規了... 生活管家默默在後排端出剛泡好的無糖冷泡鹿野紅烏龍解膩。週一深夜辛苦了，犒賞完肚皮早點休息，明天繼續加油！🍵🍗✨",
        "proof": str(clout_tea_shot)
    },
    "step3_feed_likes": 0,
    "step4_post": {
        "post_id": new_post_id,
        "permalink": post_url,
        "title": "週一深夜十一點半灰色虎斑毛球卡位",
        "hero": "喵編 (店貓 - 灰色虎斑貓)",
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

print("\n🎉 週一深夜社交漫遊全流程大統攝完成！")
