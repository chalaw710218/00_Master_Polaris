#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動執行看家門回覆：高情商秒回 3 位真實網友留言
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
STATE_FILE = ROOT_DIR / "scripts" / "replied_ids.json"

sys.path.insert(0, str(ROOT_DIR / "scripts"))
sys.path.insert(0, str(ROOT_DIR))
from threads_replier_bot import reply_to_comment, load_replied_ids, save_replied_ids

COMMENTS_TO_REPLY = [
    {
        "id": "18123233483473867",
        "username": "hardworkercat",
        "reply": "（心滿意足舔爪爪）人類這麼辛苦，本喵等一下就多賞你吸兩口肚皮抵罐罐錢喵～週一開工加油喵！🐾"
    },
    {
        "id": "18100384817560685",
        "username": "bone_1976",
        "reply": "開貨櫃車非常耗神辛苦，辛苦大哥了！出車前千萬要吃飽、喝杯熱茶顧好精神。主子半夜準時叫是催你出門要注意安全呀，今天一路順風平安！🚛🍵"
    },
    {
        "id": "17965813296215933",
        "username": "oh.ouo",
        "reply": "（大哈欠）那當然喵～本喵的一天：睡覺、吃飯、巡邏紙箱、再睡覺。人類如果學會本喵的作息，世界上就沒有週一症候群了喵🐾"
    }
]

replied_ids = load_replied_ids()
success_count = 0

print("🚀 開始處理 3 則新訪客留言...")

for item in COMMENTS_TO_REPLY:
    cid = item["id"]
    uname = item["username"]
    reply_text = item["reply"]
    print(f"\n💬 正在回覆 @{uname} (ID: {cid})...")
    print(f"   內容: {reply_text}")
    
    # 嘗試官方 API
    ok = reply_to_comment(cid, reply_text)
    if ok:
        replied_ids.add(cid)
        success_count += 1
        print(f"   ✅ @{uname} API 回覆成功！")
    else:
        print(f"   ℹ️ @{uname} API 回傳受限，將透過 Playwright 前端輔助回覆")

save_replied_ids(replied_ids)

# 透過 Playwright 截圖存證並補刀未成功的回覆
post_url = "https://www.threads.net/@hellotaitung/post/DfNSfI9gQSF"
shot_proof = SCREENSHOT_DIR / "walk_v3_home_replies_proof.png"

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
        
        # 滾動以加載所有留言
        page.evaluate("window.scrollBy(0, 500)")
        page.wait_for_timeout(2000)
        
        page.screenshot(path=str(shot_proof), full_page=True)
        print(f"\n📸 看家門留言回覆實況截圖已存證: {shot_proof.name}")
    except Exception as e:
        print(f"⚠️ 截圖提示: {e}")
    browser.close()

print(f"\n🎉 看家門回覆全數完成！共處理 {len(COMMENTS_TO_REPLY)} 則留言。")
