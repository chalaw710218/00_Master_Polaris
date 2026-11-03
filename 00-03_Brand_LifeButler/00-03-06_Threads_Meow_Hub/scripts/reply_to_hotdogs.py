#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
立即回覆 @hotdogs._0315 的留言並留證
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

COMMENT_ID = "18412533202093822"
POST_ID = "18389247586225970"
USERNAME = "hotdogs._0315"
REPLY_TEXT = "喵嗚！感謝 @hotdogs._0315 推薦！🐾 黏飯機是什麼神奇魔法～身為專業試吃官，本喵這就把這款貓糧列入清單，等等督促闆仔奉上試吃報告！睡眠不足真的太需要被主子治癒了，只要貓貓肯乖乖吃飯打呼嚕，人類的疲勞就一筆勾銷了喵～😻"

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
shot_path = SCREENSHOT_DIR / "walk_v3_reply_hotdogs_proof.png"

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
