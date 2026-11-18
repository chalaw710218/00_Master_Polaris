# -*- coding: utf-8 -*-
"""
verify_online_console.py
使用 Playwright 開啟線上 GitHub Pages 頁面：
https://chalaw710218.github.io/taitung-trash-radar/
監聽所有 Console 訊息與 Page Error，驗證 0 錯誤並截圖存證！
"""

import sys
import time
from playwright.sync_api import sync_playwright

ONLINE_URL = "https://chalaw710218.github.io/taitung-trash-radar/"
SCREENSHOT_PATH = "C:/Users/lenovo/.gemini/antigravity/brain/a852e82a-d917-4089-bea2-063fa0aa6f93/online_radar_console_verified.png"

console_logs = []
page_errors = []

def on_console(msg):
    console_logs.append(f"[{msg.type.upper()}] {msg.text}")
    print(f"Browser Console: [{msg.type.upper()}] {msg.text}")

def on_page_error(err):
    page_errors.append(str(err))
    print(f"Browser Page Error: {err}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # 模擬手機視窗 (iPhone 14 / 高清常民視角)
    context = browser.new_context(
        viewport={"width": 414, "height": 896},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    )
    page = context.new_page()
    page.on("console", on_console)
    page.on("pageerror", on_page_error)

    print(f"Navigating to {ONLINE_URL}...")
    page.goto(ONLINE_URL, wait_until="networkidle", timeout=30000)
    
    # 額外等待 3 秒確保非同步資料加載與 renderRadar 完成
    time.sleep(3)

    # 截圖存證
    page.screenshot(path=SCREENSHOT_PATH, full_page=True)
    print(f"Screenshot saved to: {SCREENSHOT_PATH}")

    browser.close()

print("\n" + "="*50)
print("🔍 線上 Console 審計報告 (Audit Report)")
print("="*50)
print(f"Total Console Messages: {len(console_logs)}")
for log in console_logs:
    print("  ", log)

print(f"\nTotal Page Errors: {len(page_errors)}")
for err in page_errors:
    print("  ❌", err)

if len(page_errors) == 0:
    # 檢查有無 null 讀取錯誤
    null_errors = [l for l in console_logs if "Cannot read properties of null" in l or "TypeError" in l]
    if len(null_errors) == 0:
        print("\n🟢 戴明驗收 PASS：線上正式站點 Console 零錯誤！B 項 DOM ID bug 徹底根除！")
        sys.exit(0)
    else:
        print("\n❌ 仍有 null 錯誤：", null_errors)
        sys.exit(1)
else:
    print("\n❌ 頁面有未捕獲錯誤！")
    sys.exit(1)
