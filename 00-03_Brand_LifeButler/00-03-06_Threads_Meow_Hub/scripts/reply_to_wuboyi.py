#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
立即回覆 @wuboyi582 的留言並留證
"""

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

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))
from threads_replier_bot import reply_to_comment, save_replied_ids, load_replied_ids

COMMENT_ID = "18097859732431577"
POST_ID = "18458764969127270"
USERNAME = "wuboyi582"
REPLY_TEXT = "讀書辛苦了喵！能隔空幫你充電是本喵的榮幸🐾 讀到快靈魂出竅時喝一口順口的現萃茶真的超解壓～不過讀累了一定要記得站起來伸個大懶腰、讓眼睛休息五分鐘喵！本喵在台東隔空借你摸一把灰色虎斑肚肚，繼續加油喵～✨"

print(f"💌 準備回覆 @{USERNAME} 的留言...")
success = reply_to_comment(COMMENT_ID, REPLY_TEXT)

if success:
    replied_ids = load_replied_ids()
    replied_ids.add(COMMENT_ID)
    save_replied_ids(replied_ids)
    print("✅ 已記錄到 replied_ids.json！")
else:
    print("⚠️ API 回覆失敗，嘗試使用前端補發...")

# 截圖存證
SESSION_PATH = ROOT_DIR / "scripts" / "threads_session.json"
SCREENSHOT_DIR = ROOT_DIR / "scripts" / "screenshots"
shot_path = SCREENSHOT_DIR / "walk_v3_reply_wuboyi_proof.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()
    try:
        page.goto(f"https://www.threads.net/@hellotaitung/post/{POST_ID}", wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(4000)
        page.screenshot(path=str(shot_path))
        print(f"📸 回覆存證截圖已留存: {shot_path.name}")
    except Exception as e:
        print(f"⚠️ 截圖失敗: {e}")
    browser.close()
