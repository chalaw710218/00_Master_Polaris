#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 全自動海巡點愛心與互動機器人 (Threads Auto Patrol & Liker)
北極星專屬全自動社交工具
作者: 影 (Shadow)
"""

import os
import sys
import time
import random
import argparse
from pathlib import Path

# 確保 Windows 終端機支援 Emoji
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
SCREENSHOT_DIR = SCRIPT_DIR / "screenshots"

def create_browser_context(playwright, headless=True):
    """建立攜帶登入憑證的瀏覽器 context"""
    browser = playwright.chromium.launch(
        headless=headless,
        args=["--disable-blink-features=AutomationControlled"]
    )
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        locale="zh-TW",
        viewport={"width": 1280, "height": 800}
    )
    return browser, context

def like_post_url(post_url, headless=True):
    """針對單一貼文網址點愛心"""
    from playwright.sync_api import sync_playwright

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    print(f"🎯 [點讚任務] 前往目標貼文: {post_url}")

    with sync_playwright() as p:
        browser, context = create_browser_context(p, headless=headless)
        page = context.new_page()

        try:
            page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)

            # 尋找愛心按鈕 (Like / 讚)
            like_btn = None
            for sel in [
                'svg[title="Like"]',
                'svg[title="讚"]',
                'div[role="button"]:has(svg[title="Like"])',
                'div[role="button"]:has(svg[title="讚"])',
                'div[role="button"]:has(svg[aria-label="Like"])',
                'div[role="button"]:has(svg[aria-label="讚"])',
                'svg[aria-label="Like"]',
                'svg[aria-label="讚"]'
            ]:
                loc = page.locator(sel)
                if loc.count() > 0 and loc.first.is_visible():
                    like_btn = loc.first
                    break

            # 檢查是否已經點過讚 (Unlike / 收回讚)
            already_liked = False
            for sel in [
                'svg[title="Unlike"]',
                'svg[title="收回讚"]',
                'svg[aria-label="Unlike"]',
                'svg[aria-label="收回讚"]',
                'div[role="button"]:has(svg[title="Unlike"])',
                'div[role="button"]:has(svg[title="收回讚"])'
            ]:
                loc = page.locator(sel)
                if loc.count() > 0 and loc.first.is_visible():
                    already_liked = True
                    break

            if already_liked:
                print("💖 此貼文已經點過愛心囉！不需重複點擊。")
                screenshot_path = SCREENSHOT_DIR / "already_liked.png"
                page.screenshot(path=str(screenshot_path))
                browser.close()
                return True

            if like_btn:
                print("❤️ 找到愛心按鈕，正在點擊...")
                like_btn.click(timeout=4000, force=True)
                page.wait_for_timeout(2000)
                screenshot_path = SCREENSHOT_DIR / "like_success.png"
                page.screenshot(path=str(screenshot_path))
                print(f"🎉 點讚成功！截圖已保存: {screenshot_path}")
                browser.close()
                return True
            else:
                print("⚠️ 找不到未點擊的愛心按鈕。截圖備查...")
                screenshot_path = SCREENSHOT_DIR / "like_btn_not_found.png"
                page.screenshot(path=str(screenshot_path))
                browser.close()
                return False

        except Exception as e:
            print(f"❌ 點讚過程發生例外: {e}")
            browser.close()
            return False

def patrol_feed_and_like(max_likes=5, scroll_times=3, headless=True):
    """
    全自動首頁海巡點讚：
    進入 Threads 首頁動態牆，自動向下滾動，識別未點讚的貼文並給予愛心 ❤️
    :param max_likes: 單次海巡最多點讚篇數 (防濫用安全閾值)
    :param scroll_times: 向下滾動次數
    """
    from playwright.sync_api import sync_playwright

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    print("==================================================")
    print("🌊 [北極星 Threads 全自動動態牆海巡點讚機]")
    print(f"🎯 目標設定: 單次上限 {max_likes} 個愛心，滾動巡邏 {scroll_times} 次")
    print("==================================================")

    if not SESSION_PATH.exists():
        print("❌ 找不到登入憑證！請先執行 threads_web_login.py")
        return 0

    likes_count = 0

    with sync_playwright() as p:
        browser, context = create_browser_context(p, headless=headless)
        page = context.new_page()

        try:
            print("🌐 正在進入 Threads 首頁動態牆...")
            page.goto("https://www.threads.net/", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(4000)

            for scroll_idx in range(scroll_times):
                if likes_count >= max_likes:
                    print(f"🛑 已達到單次點讚上限 ({max_likes} 篇)，守護帳號健康。")
                    break

                print(f"\n🔍 [第 {scroll_idx + 1}/{scroll_times} 輪海巡掃描中...]")

                # 精確鎖定包含未點讚愛心之按鈕容器 (避免重複選取與指標攔截)
                like_buttons = page.locator('div[role="button"]:has(> div svg[title="Like"]), div[role="button"]:has(> div svg[title="讚"]), div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])')
                count = like_buttons.count()
                print(f"👀 當前畫面上發現 {count} 個待點讚貼文按鈕")

                for i in range(count):
                    if likes_count >= max_likes:
                        break

                    btn = like_buttons.nth(i)
                    if btn.is_visible():
                        try:
                            # 隨機停留 1.5~3 秒模擬真人閱讀節奏
                            delay = random.uniform(1.5, 3.0)
                            print(f"⏳ 模擬閱讀停留 {delay:.1f} 秒...")
                            time.sleep(delay)

                            btn.click(timeout=3000, force=True)
                            likes_count += 1
                            print(f"❤️ [成功送出第 {likes_count} 顆愛心！]")
                            page.wait_for_timeout(1000)
                        except Exception as click_err:
                            print(f"⚠️ 點擊失敗或跳過: {click_err}")

                # 模擬人類向下滾動動態牆
                scroll_distance = random.randint(500, 900)
                print(f"📜 向下滾動瀏覽 {scroll_distance}px...")
                page.mouse.wheel(0, scroll_distance)
                page.wait_for_timeout(2500)

            screenshot_path = SCREENSHOT_DIR / "patrol_summary.png"
            page.screenshot(path=str(screenshot_path))
            print("\n==================================================")
            print(f"🎉 [海巡任務圓滿完成] 共送出 {likes_count} 顆愛心！")
            print(f"📸 巡邏終端截圖已存檔: {screenshot_path}")
            print("==================================================")

        except Exception as e:
            print(f"❌ 海巡過程發生例外: {e}")
        finally:
            browser.close()

    return likes_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Threads 自動點愛心與海巡機")
    parser.add_argument("--url", type=str, help="指定貼文網址點愛心")
    parser.add_argument("--feed", action="store_true", help="執行首頁動態牆自動海巡點讚")
    parser.add_argument("--max", type=int, default=3, help="動態牆海巡最大點讚數 (預設 3)")
    parser.add_argument("--headful", action="store_true", help="開啟可見瀏覽器 (預設無頭模式)")

    args = parser.parse_args()

    headless_mode = not args.headful

    if args.url:
        like_post_url(args.url, headless=headless_mode)
    else:
        # 預設執行首頁動態牆海巡
        patrol_feed_and_like(max_likes=args.max, scroll_times=3, headless=headless_mode)
