# -*- coding: utf-8 -*-
"""
verify_production_online.py
直接連線 GitHub Pages 正式站點進行實機驗收：
1. 訪問 https://chalaw710218.github.io/taitung-trash-radar/
2. 注入 __TEST_NOW__ 為週一 17:00
3. 監聽 Console 與 Network 請求
4. 點擊 #recycleBox 勾選雙收
5. 捕捉增量發出的 /schedule?run_id=1618 請求
6. 截圖存入 05_Trash_Radar_Engine/evidence/online_network_recycle_verified.png
7. 日誌存入 05_Trash_Radar_Engine/evidence/online_network_recycle_requests.json
"""

import json
import os
import sys
import time
from playwright.sync_api import sync_playwright

ENGINE_DIR = os.path.abspath("05_Trash_Radar_Engine")
EVIDENCE_DIR = os.path.join(ENGINE_DIR, "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

SCREENSHOT_PATH = os.path.join(EVIDENCE_DIR, "online_network_recycle_verified.png")
LOG_PATH = os.path.join(EVIDENCE_DIR, "online_network_recycle_requests.json")

ONLINE_URL = "https://chalaw710218.github.io/taitung-trash-radar/"

captured_schedules = []
console_logs = []

def on_request(req):
    if "/schedule" in req.url:
        print(f"📡 [ONLINE SCHEDULE] {req.method} {req.url}")
        captured_schedules.append(req.url)

def on_console(msg):
    console_logs.append(f"[{msg.type}] {msg.text}")

print(f"Connecting to production site: {ONLINE_URL} ...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 414, "height": 896},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15"
    )
    page = context.new_page()
    page.on("request", on_request)
    page.on("console", on_console)
    page.on("pageerror", lambda err: console_logs.append(f"[pageerror] {err}"))

    # 模擬週一出勤時段
    page.add_init_script("window.__TEST_NOW__ = '2026-11-16T17:00:00+08:00';")

    page.goto(ONLINE_URL)
    # 等待初始資源加載
    time.sleep(6)

    init_count = len(captured_schedules)
    print(f"Initial schedule requests count: {init_count}")

    # 清空列表，準備精確捕捉點擊雙收後的增量請求
    captured_schedules.clear()

    print("\n👉 Clicking #recycleBox to toggle Recycling ON on production site...")
    page.click("#recycleBox")

    # 等待雙收回收車路線請求發出 (最多等 10 秒)
    start_t = time.time()
    while time.time() - start_t < 10:
        if any("run_id=1618" in u for u in captured_schedules):
            break
        time.sleep(0.5)

    print(f"\nCaptured post-toggle schedule requests: {len(captured_schedules)}")
    for u in captured_schedules:
        print("  🟢 Captured:", u)

    # 截圖存檔
    page.screenshot(path=SCREENSHOT_PATH, full_page=True)
    print(f"📸 Screenshot saved to: {SCREENSHOT_PATH}")

    browser.close()

with open(LOG_PATH, "w", encoding="utf-8") as f:
    json.dump({
        "url": ONLINE_URL,
        "captured_schedules": captured_schedules,
        "has_1618": any("run_id=1618" in u for u in captured_schedules),
        "console_logs": console_logs
    }, f, ensure_ascii=False, indent=2)

print(f"📝 Online test log saved to: {LOG_PATH}")

has_1618 = any("run_id=1618" in u for u in captured_schedules)
if has_1618:
    print("🟢 線上真實驗收 100% PASS：GitHub Pages 正式站點點擊雙收，成功即時發出 /schedule?run_id=1618 請求！")
    sys.exit(0)
else:
    print("❌ 線上驗收尚未捕捉到 1618，可能 GitHub Pages 還在 CDN 快取更新中...")
    sys.exit(1)
