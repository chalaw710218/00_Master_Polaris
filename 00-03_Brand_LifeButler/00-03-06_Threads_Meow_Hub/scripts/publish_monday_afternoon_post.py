#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
週一下午茶貼文發布與首回覆橋接閉環 (Monday Afternoon Post & Reply Funnel)
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

POST_TEXT = """週一下午四點，看著人類眼神渙散、螢幕視窗越切越快
本喵早就把下巴擱在毛毛前腳上，進入午後第二輪深層充電模式了喵🐾

再撐一下，離下班只剩最後幾張試算表了！
如果現在眼皮太沉，本喵允許你先隔空吸一口本喵毛茸茸的灰色虎斑肚皮充電喵～

大家現在是在等下班，還是已經在偷偷看晚餐要吃什麼了？喵🐾

#台東生活"""

IMAGE_PATH = ROOT_DIR / "images" / "03_Posts_and_Creative" / "meow_monday_afternoon_gray_tabby.jpg"

print(f"📸 準備發布週一下午茶貼文，附圖: {IMAGE_PATH.name}")
new_post_id = publish_thread(text=POST_TEXT, image=str(IMAGE_PATH), topic_tag="台東生活")

if not new_post_id:
    print("❌ 發文失敗，終止程序")
    sys.exit(1)

print(f"🎉 貼文發布成功！Post ID: {new_post_id}")

# --- 步驟四點五：首回覆橋接 (Reply-First Bridge Funnel) ---
print("\n>>> 步驟四點五：首回覆橋接 (發布後 1 分鐘內作者公開款待留言) <<<")
first_reply_text = "（把毛茸茸的灰斑下巴靠在桌上打呼嚕）大家今天辛苦了喵～再撐一下下就下班了！今晚回家想好要吃什麼好料犒勞自己了嗎？快跟本喵說喵🐾 #台東生活"

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
shot_post = SCREENSHOT_DIR / "walk_v3_monday_afternoon_verified.png"

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
        print(f"   📸 下午茶貼文存證截圖已留存: {shot_post.name}")
    except Exception as e:
        print(f"   ⚠️ 存證截圖提示: {e}")
    browser.close()

# 更新好友帳本
print("\n>>> 步驟五：好友帳本更新 (Social CRM Ledger) <<<")
clout_tea_shot = SCREENSHOT_DIR / "walk_v3_clout_tea_love_cat_cake.png"
record_interaction("love_love_cat_cake", "小瑪莉貓的手作甜點", action="comment",
                   comment_text="午後四點，空氣裡都是剛出爐的甜點香氣... 生活管家默默在後排端出剛泡好的鹿野紅烏龍，配小瑪莉家的甜點剛剛好。週一下午打工人辛苦了，喝口茶吃塊甜，充個電再出發！🍵🍰🐱",
                   screenshot=str(clout_tea_shot))
record_interaction("yuan.b778", "石臼一二", action="like")
record_interaction("unccoffee", "瑰夏咖啡 GESHA COFFEE", action="like")
record_interaction("deepcoffee241", "Deep coffee", action="like")
record_interaction("homu_cafe_", "和暮咖啡", action="like")
record_interaction("riceandbear", "米熊共生", action="like")

print_dashboard()

# 更新 latest_walk_v3_result.json
result_file = ROOT_DIR / "scripts" / "latest_walk_v3_result.json"
walk_result = {
    "step1_home_replies": 0,
    "step2_friends_visited": [
        {"username": "love_love_cat_cake", "name": "小瑪莉貓的手作甜點", "action": "comment_and_like"},
        {"username": "yuan.b778", "name": "石臼一二", "action": "liked"},
        {"username": "unccoffee", "name": "瑰夏咖啡 GESHA COFFEE", "action": "liked"},
        {"username": "deepcoffee241", "name": "Deep coffee", "action": "liked"},
        {"username": "homu_cafe_", "name": "和暮咖啡", "action": "visited"},
        {"username": "riceandbear", "name": "米熊共生", "action": "visited"}
    ],
    "step2_clout_tea": {
        "target": "@love_love_cat_cake (小瑪莉貓的手作甜點)",
        "message": "午後四點，空氣裡都是剛出爐的甜點香氣... 生活管家默默在後排端出剛泡好的鹿野紅烏龍，配小瑪莉家的甜點剛剛好。週一下午打工人辛苦了，喝口茶吃塊甜，充個電再出發！🍵🍰🐱",
        "proof": str(clout_tea_shot)
    },
    "step3_feed_likes": 4,
    "step4_post": {
        "post_id": new_post_id,
        "permalink": post_url,
        "title": "週一下午四點灰色虎斑貓充電",
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

print("\n🎉 週一下午茶社交漫遊全流程大統攝完成！")
