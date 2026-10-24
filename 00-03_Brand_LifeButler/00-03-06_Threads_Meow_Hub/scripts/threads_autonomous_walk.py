#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 全自動社交漫遊引擎 (Autonomous Social Walk)
當創辦人說「去逛逛」時，全自動執行閉環：
1. 巡邏友店帳號（慢食節、在地友好店家等），贈送愛心並發表走心回覆。
2. 巡邏首頁動態，隨機點讚友好在地貼文。
3. 檢查自家通知，回覆新留言。
4. (可選) 自動發布一篇符合在地氛圍的喵編日記/觀察。
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
SESSION_PATH = ROOT_DIR / "scripts" / "threads_session.json"
SCREENSHOT_DIR = ROOT_DIR / "scripts" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def engage_friend_post(page, url, comment_text, friend_name="友店"):
    print(f"\n[社交漫遊] 拜訪 {friend_name}: {url}")
    page.goto(url, wait_until='networkidle')
    page.wait_for_timeout(3000)

    # 1. 贈送愛心
    try:
        like_btn = page.locator('svg[aria-label*="讚"]').first
        if like_btn.is_visible() and "收回讚" not in (like_btn.get_attribute("aria-label") or ""):
            like_btn.click()
            print(f" -> 已為 {friend_name} 主貼文點亮愛心 ❤️")
            page.wait_for_timeout(1000)
    except Exception as e:
        print(f" -> 點讚提示: {e}")

    # 2. 點擊輸入框
    box = page.locator('div[contenteditable="true"]').first
    if not box.is_visible():
        page.evaluate("window.scrollBy(0, 300)")
        page.wait_for_timeout(1000)
        box = page.locator('div[contenteditable="true"]').first

    box.click()
    page.wait_for_timeout(500)

    # 3. 輸入文字
    print(f" -> 輸入暖心留言: {comment_text}")
    page.keyboard.type(comment_text, delay=20)
    page.wait_for_timeout(1000)

    # 4. 點擊發布箭頭按鈕
    box_rect = box.bounding_box()
    for svg in page.locator('svg').all():
        b = svg.bounding_box()
        if b and box_rect and abs(b['y'] - box_rect['y']) < 35 and b['x'] > box_rect['x']:
            svg.click(force=True)
            page.wait_for_timeout(2500)
            break

    # 5. 若彈出確認模態框，點擊「發佈」
    modal_btn = page.locator('div[role="button"]:has-text("發佈"), button:has-text("發佈")')
    if modal_btn.count() > 0:
        modal_btn.last.click(force=True)
        page.wait_for_timeout(4000)

    clean_name = friend_name.replace(" ", "_")
    shot_path = SCREENSHOT_DIR / f"walk_reply_{clean_name}.png"
    page.screenshot(path=str(shot_path))
    print(f" -> 留言完成並留存證明: {shot_path.name}")
    return str(shot_path)

def walk_and_like_feed(page, max_likes=3):
    print(f"\n[社交漫遊] 漫遊首頁動態，預計點讚 {max_likes} 篇...")
    page.goto('https://www.threads.com/', wait_until='networkidle')
    page.wait_for_timeout(3000)

    likes_done = 0
    for scroll in range(5):
        like_buttons = page.locator('svg[aria-label="讚"]').all()
        for btn in like_buttons:
            if likes_done >= max_likes:
                break
            try:
                b = btn.bounding_box()
                if b and b['y'] > 150 and b['y'] < 900:
                    btn.click()
                    likes_done += 1
                    print(f" -> 漫遊點讚第 {likes_done}/{max_likes} 篇 ❤️")
                    page.wait_for_timeout(1500)
            except Exception:
                continue

        if likes_done >= max_likes:
            break
        page.evaluate("window.scrollBy(0, 800)")
        page.wait_for_timeout(2000)

    print(f" -> 首頁漫遊點讚完成，共送出 {likes_done} 顆愛心。")

if __name__ == "__main__":
    if not SESSION_PATH.exists():
        print("Error: threads_session.json not found.")
        sys.exit(1)

    print("=== 極星 Threads 自動社交漫遊引擎啟動 ===")
