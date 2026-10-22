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

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
SCREENSHOT_DIR = SCRIPT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

def inspect_all_activity():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_PATH),
            viewport={"width": 1280, "height": 900},
            locale="zh-TW"
        )
        page = context.new_page()
        print("🌐 前往 https://www.threads.com/activity ...")
        page.goto("https://www.threads.com/activity", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(4000)

        # 截圖「全部動態」
        page.screenshot(path=str(SCREENSHOT_DIR / "activity_feed_all.png"))
        print("📸 已截圖：activity_feed_all.png")

        # 點擊「動態 提及 v」或「動態 全部 v」下拉選單
        filter_btn = page.locator('div[role="button"]:has-text("動態"), span:has-text("動態")').first
        if filter_btn.is_visible():
            print("🔽 點擊動態分類下拉選單...")
            filter_btn.click(force=True)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(SCREENSHOT_DIR / "activity_dropdown.png"))
            print("📸 已截圖：activity_dropdown.png")

            # 點擊「回覆」
            reply_option = page.locator('div[role="menuitem"]:has-text("回覆"), span:has-text("回覆"), div[role="button"]:has-text("回覆")')
            if reply_option.count() > 0:
                print("💬 點擊『回覆』分類...")
                reply_option.first.click(force=True)
                page.wait_for_timeout(3000)
                page.screenshot(path=str(SCREENSHOT_DIR / "activity_feed_replies.png"))
                print("📸 已截圖：activity_feed_replies.png")

        browser.close()

if __name__ == "__main__":
    inspect_all_activity()
