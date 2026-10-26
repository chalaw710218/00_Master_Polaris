#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 全自動社交漫遊總控腳本 (Autonomous Social Walk Master)
由 .agents/skills/threads-autonomous-walker 調用。
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

# 定位主工作目錄與資源
BASE_HUB = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub")
if str(BASE_HUB) not in sys.path:
    sys.path.insert(0, str(BASE_HUB))

# 引入好友帳本模組
try:
    from scripts.friend_ledger import record_interaction, recommend_next, print_dashboard
except ImportError:
    try:
        from friend_ledger import record_interaction, recommend_next, print_dashboard
    except Exception as e:
        print(f"Warning: could not import friend_ledger: {e}")
        record_interaction = lambda **kwargs: None
        recommend_next = lambda n: []
        print_dashboard = lambda: None

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 定位主工作目錄與資源
BASE_HUB = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub")
SESSION_PATH = BASE_HUB / "scripts" / "threads_session.json"
TARGETS_PATH = BASE_HUB / "scripts" / "following_targets.json"
SCREENSHOT_DIR = BASE_HUB / "scripts" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = BASE_HUB / "data" / "walk_history.jsonl"
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_action(action_type, details):
    record = {
        "timestamp": datetime.now().isoformat(),
        "type": action_type,
        "details": details
    }
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def engage_friend_post(page, url, comment_text, friend_name="友店"):
    print(f"\n[訪友] 拜訪 {friend_name}: {url}")
    try:
        page.goto(url, wait_until='networkidle')
        page.wait_for_timeout(3000)
    except Exception as e:
        print(f" -> 導航超時或失敗: {e}")
        return None

    # 1. 贈送愛心
    try:
        like_btn = page.locator('svg[aria-label*="讚"]').first
        if like_btn.is_visible() and "收回讚" not in (like_btn.get_attribute("aria-label") or ""):
            like_btn.click()
            print(f" -> 已為 {friend_name} 主貼文點亮愛心 ❤️")
            page.wait_for_timeout(1000)
            log_action("like_friend_post", {"friend": friend_name, "url": url})
        else:
            print(" -> 貼文已點讚或無讚按鈕")
    except Exception as e:
        print(f" -> 點讚處理提示: {e}")

    # 2. 點擊輸入框
    box = page.locator('div[contenteditable="true"]').first
    if not box.is_visible():
        page.evaluate("window.scrollBy(0, 300)")
        page.wait_for_timeout(1000)
        box = page.locator('div[contenteditable="true"]').first

    if not box.is_visible():
        print(" -> 未找到輸入框，跳過留言")
        return None

    box.click()
    page.wait_for_timeout(500)

    # 3. 輸入文字
    print(f" -> 輸入走心留言: {comment_text}")
    page.keyboard.type(comment_text, delay=20)
    page.wait_for_timeout(1000)

    # 4. 點擊膠囊內的發布箭頭 (鎖定寬度 >20 且位於膠囊右側之黑色圓形送出按鈕)
    send_btn = None
    for btn in page.locator('div[role="button"], button').all():
        b = btn.bounding_box()
        if b and 880 < b['x'] < 960 and b['y'] > 850 and b['width'] > 20:
            send_btn = btn
            break

    if send_btn:
        print(" -> 點擊送出箭頭按鈕...")
        send_btn.click(force=True)
    else:
        print(" -> 依精確坐標點擊送出按鈕 (916, 990)...")
        page.mouse.click(916, 990)

    page.wait_for_timeout(3000)

    # 5. 若打開了回覆彈窗，點擊「發佈」按鈕
    modal_btn = page.locator('div[role="button"]:has-text("發佈"), button:has-text("發佈")')
    if modal_btn.count() > 0:
        print(" -> 點擊彈窗發佈按鈕...")
        modal_btn.last.click(force=True)
        page.wait_for_timeout(5000)
    else:
        page.wait_for_timeout(4000)

    clean_name = friend_name.replace(" ", "_").replace("@", "")
    shot_path = SCREENSHOT_DIR / f"walk_reply_{clean_name}.png"
    page.screenshot(path=str(shot_path))
    print(f" -> 留言完成並保存驗證截圖: {shot_path.name}")
    log_action("comment_friend_post", {"friend": friend_name, "comment": comment_text, "screenshot": str(shot_path)})
    
    # 同步寫入極星社群好友帳本
    try:
        record_interaction(
            username=friend_name,
            name=friend_name,
            action="like_and_comment",
            post_url=url,
            comment_text=comment_text,
            screenshot=str(shot_path)
        )
    except Exception as e:
        print(f" -> 寫入好友帳本提示: {e}")

    return str(shot_path)

def walk_feed(page, max_likes=3):
    print(f"\n[漫遊] 漫步 Threads 首頁推薦，預計贈送 {max_likes} 顆愛心...")
    try:
        page.goto('https://www.threads.com/', wait_until='networkidle')
        page.wait_for_timeout(3000)
    except Exception as e:
        print(f" -> 首頁載入失敗: {e}")
        return 0

    likes_done = 0
    for scroll in range(5):
        like_buttons = page.locator('svg[aria-label="讚"]').all()
        for btn in like_buttons:
            if likes_done >= max_likes:
                break
            try:
                b = btn.bounding_box()
                if b and 150 < b['y'] < 900:
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

    log_action("feed_likes", {"count": likes_done})
    print(f" -> 首頁動態漫遊完成，共送出 {likes_done} 顆愛心。")
    return likes_done

def main():
    parser = argparse.ArgumentParser(description="Threads 全自動社交漫遊總控")
    parser.add_argument("--all", action="store_true", help="執行全套漫遊（看家、訪友、點讚、帳本顯示）")
    parser.add_argument("--friends", action="store_true", help="僅執行友店巡邏與互動")
    parser.add_argument("--feed", action="store_true", help="僅執行首頁動態按愛心")
    parser.add_argument("--ledger", action="store_true", help="直接顯示好友互動帳本與關係溫度")
    parser.add_argument("--max-likes", type=int, default=3, help="首頁漫遊點讚數量 (預設 3)")
    args = parser.parse_args()

    if args.ledger:
        print_dashboard()
        recommend_next(3)
        return

    if not SESSION_PATH.exists():
        print(f"Error: Session file not found at {SESSION_PATH}")
        sys.exit(1)

    # 預設執行全套
    run_friends = args.all or args.friends or (not args.feed)
    run_feed = args.all or args.feed or (not args.friends)

    print("==================================================")
    print("🐾 極星 Threads 全自動社交漫遊 (Social Walk) 啟動")
    print("==================================================")

    # 友店預設常規拜訪標的 (可動態擴充或結合 RSS)
    SAMPLE_TARGETS = [
        {
            "name": "臺東慢食節",
            "url": "https://www.threads.com/@slowfoodtaitung",
            "default_comment": "安全第一！大家一起期待開桌，喵編已經準備好肚子了喵 🍖🐾"
        },
        {
            "name": "Hatt Coffee",
            "url": "https://www.threads.com/@hattcoffee",
            "default_comment": "老闆辛苦了！祝順利突破目標，喵編等好天氣再去喝一杯喵 ☕🐾"
        }
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_PATH),
            viewport={'width': 1280, 'height': 1000},
            locale='zh-TW'
        )
        page = context.new_page()

        if run_friends:
            print("\n>>> 階段：訪友與走心社交 <<<")
            # 這裡可遍歷指定標的
            for t in SAMPLE_TARGETS:
                # 可以在實際調用時傳入具體貼文 URL
                pass

        if run_feed:
            print("\n>>> 階段：首頁推薦動態漫遊 <<<")
            walk_feed(page, max_likes=args.max_likes)

        browser.close()

    print("\n✅ 漫遊閉環執行完畢！")
    
    # 自動附帶顯示最新好友帳本與下次漫遊建議
    try:
        print_dashboard()
        recommend_next(3)
    except Exception as e:
        print(f"提示: 好友帳本顯示未執行: {e}")

if __name__ == "__main__":
    main()
