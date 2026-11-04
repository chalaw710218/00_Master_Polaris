#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
專屬執行 Deep Coffee 借光端茶並截圖
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
SESSION_PATH = ROOT_DIR / "scripts" / "threads_session.json"
SCREENSHOT_DIR = ROOT_DIR / "scripts" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_USERNAME = "deepcoffee241"
TARGET_NAME = "Deep coffee"
MESSAGE = "週三早上九點半，剛走進辦公室最需要一杯深烘焙的手沖黑咖啡醒腦... 生活管家默默在後排端出剛泡好的鹿野紅烏龍熱茶。今天已經是週三小週末了，深呼吸一口氣，喝口好咖啡，離放假只剩一半路程了！🍵☕🍞"
PROOF_PATH = SCREENSHOT_DIR / "walk_v3_clout_tea_deepcoffee.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()
    try:
        print(f"🍵 正在前往 @{TARGET_USERNAME} 借光端茶...")
        page.goto(f"https://www.threads.net/@{TARGET_USERNAME}", wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3500)

        reply_btn = page.locator('svg[aria-label="回覆"], svg[aria-label="Reply"]').first
        if reply_btn.is_visible(timeout=3000):
            reply_btn.click()
            page.wait_for_timeout(1000)
            input_box = page.locator('div[contenteditable="true"], div[role="textbox"]').first
            if input_box.is_visible(timeout=3000):
                input_box.click()
                page.keyboard.type(MESSAGE, delay=20)
                page.wait_for_timeout(1000)
                post_btn = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("Post")').first
                if post_btn.is_visible(timeout=2000):
                    post_btn.click()
                    page.wait_for_timeout(3000)
        
        page.screenshot(path=str(PROOF_PATH))
        print(f"📸 借光端茶截圖成功: {PROOF_PATH.name}")
    except Exception as e:
        print(f"⚠️ 提示: {e}")
        try:
            page.screenshot(path=str(PROOF_PATH))
        except Exception:
            pass
    browser.close()
