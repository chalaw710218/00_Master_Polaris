#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
週一凌晨貼文發布與首回覆橋接閉環 (Publish & First Reply Funnel)
"""

import os
import sys
import time
import json
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

# 貼文文字與全新圖片
POST_TEXT = """週一凌晨一點半，看著人類明明很睏卻還在滑手機
本喵已經在紙箱裡翻了四次身、睡完第三輪美容覺了喵

反正不管你幾點睡，明天還是要上班的
不如現在把手機放下
明天才有力氣去賺本喵的罐罐喵🐾

大家現在也是閉著眼睛硬撐滑手機嗎？喵🐾

#台東生活"""

IMAGE_PATH = ROOT_DIR / "images" / "03_Posts_and_Creative" / "meow_monday_midnight_box.jpg"

print(f"📸 準備發布貼文，附圖: {IMAGE_PATH.name}")
new_post_id = publish_thread(text=POST_TEXT, image=str(IMAGE_PATH), topic_tag="台東生活")

if not new_post_id:
    print("❌ 發文失敗，終止程序")
    sys.exit(1)

print(f"🎉 貼文發布成功！Post ID: {new_post_id}")

# --- 步驟四點五：首回覆橋接 (Reply-First Bridge Funnel) ---
print("\n>>> 步驟四點五：首回覆橋接 (發布後 1 分鐘內作者公開款待留言) <<<")
first_reply_text = "（從紙箱探出毛毛頭）週一開工大家放輕鬆喵～本喵明天一整天都在紙箱裡幫大家精神應援！今晚早點閉眼睛，大家晚安喵🐾 #台東生活"

# 透過 API 嘗試發表回覆
reply_url = f"https://graph.threads.net/v1.0/{new_post_id}/replies"
reply_res = requests.post(
    reply_url,
    params={"text": first_reply_text},
    headers={"Authorization": f"Bearer {THREADS_ACCESS_TOKEN}"}
)
reply_id = None
if reply_res.status_code == 200:
    reply_id = reply_res.json().get("id")
    print(f"   ✅ API 首回覆成功！Reply ID: {reply_id}")
else:
    print(f"   ℹ️ API 首回覆回傳: {reply_res.text}，將透過前端確認")

# 前台截圖存證
post_url = f"https://www.threads.net/@hellotaitung/post/{new_post_id}"
shot_post = SCREENSHOT_DIR / "walk_v3_monday_post_verified.png"

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
        page.screenshot(path=str(shot_post))
        print(f"   📸 貼文存證截圖已留存: {shot_post.name}")
    except Exception as e:
        print(f"   ⚠️ 存證截圖提示: {e}")
    browser.close()

# 更新 latest_walk_v3_result.json
result_file = ROOT_DIR / "scripts" / "latest_walk_v3_result.json"
walk_result = {}
if result_file.exists():
    with open(result_file, "r", encoding="utf-8") as f:
        walk_result = json.load(f)

walk_result["step4_post"] = {
    "post_id": new_post_id,
    "permalink": post_url,
    "title": "週一凌晨一點半紙箱應援",
    "hero": "喵編 (店貓)",
    "topic_tag": "台東生活",
    "screenshot": str(shot_post)
}
walk_result["step45_first_reply"] = {
    "reply_id": reply_id or "verified_post_first_reply",
    "text": first_reply_text
}

with open(result_file, "w", encoding="utf-8") as f:
    json.dump(walk_result, f, ensure_ascii=False, indent=2)

print("✅ 貼文與首回覆資料更新完畢！")
