# -*- coding: utf-8 -*-
"""
verify_recycle_network_requests.py
以本機 HTTP Server 提供真實 HTTP 協議服務，讓 data/ *.json 順利載入。
Playwright 實測流程：
1. 開啟 http://127.0.0.1:8765/
2. 注入 __TEST_NOW__ 為週一 17:00 (出勤時段)
3. 初始載入只倒垃圾
4. 點擊【勾選雙收】(#recycleBox)
5. 監聽 Network 請求，驗證觸發 /schedule?run_id=1618 (回KEH-5218 一、五)
6. 截圖存檔至 05_Trash_Radar_Engine/evidence/
7. 儲存網路請求日誌至 05_Trash_Radar_Engine/evidence/
"""

import http.server
import json
import os
import socketserver
import sys
import threading
import time
from playwright.sync_api import sync_playwright

ENGINE_DIR = os.path.abspath("05_Trash_Radar_Engine")
EVIDENCE_DIR = os.path.join(ENGINE_DIR, "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

SCREENSHOT_PATH = os.path.join(EVIDENCE_DIR, "network_recycle_prefetch_verified.png")
NETWORK_LOG_PATH = os.path.join(EVIDENCE_DIR, "network_recycle_requests.json")

PORT = 8765

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ENGINE_DIR, **kwargs)
    def log_message(self, format, *args):
        pass # 安靜模式

# 啟動背景 HTTP Server
httpd = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"HTTP Server started at http://127.0.0.1:{PORT}/")

captured_requests = []
recycle_schedule_requests = []

def on_request(req):
    url = req.url
    captured_requests.append({
        "url": url,
        "method": req.method,
        "timestamp": time.time()
    })
    if "/schedule" in url:
        print(f"📡 [SCHEDULE REQUEST DETECTED] {req.method} {url}")
        recycle_schedule_requests.append(url)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 414, "height": 896},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15"
        )
        page = context.new_page()
        page.on("request", on_request)

        # 模擬週一 17:00 (1618 回收車出勤日)
        page.add_init_script("window.__TEST_NOW__ = '2026-11-16T17:00:00+08:00';")

        print(f"Navigating to http://127.0.0.1:{PORT}/index.html ...")
        page.goto(f"http://127.0.0.1:{PORT}/index.html")
        # 等待初始垃圾車路線抓取完畢 (最多 10 秒)
        time.sleep(5)

        initial_count = len(recycle_schedule_requests)
        print(f"Initial schedule requests count: {initial_count}")

        # 清空列表，精準捕捉點擊【勾選雙收】後產生的增量請求
        recycle_schedule_requests.clear()

        print("\n👉 User Action: Clicking #recycleBox to toggle Recycling ON...")
        page.click("#recycleBox")
        
        # 等待並行請求觸發，直到捕捉到 1618 或最多等 10 秒
        start_wait = time.time()
        while time.time() - start_wait < 10:
            if any("run_id=1618" in u for u in recycle_schedule_requests):
                break
            time.sleep(0.5)

        print(f"\n--- Post-Toggle Schedule Requests captured: {len(recycle_schedule_requests)} ---")
        for r in recycle_schedule_requests:
            print("  🟢 Captured:", r)

        # 截圖存證至 evidence/
        page.screenshot(path=SCREENSHOT_PATH, full_page=True)
        print(f"\n📸 Screenshot saved to: {SCREENSHOT_PATH}")

        browser.close()

    # 儲存網路請求日誌
    with open(NETWORK_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "target_verified": "run_id=1618",
            "recycle_schedule_requests": recycle_schedule_requests,
            "all_captured_count": len(captured_requests)
        }, f, ensure_ascii=False, indent=2)
    print(f"📝 Network log saved to: {NETWORK_LOG_PATH}")

    # 驗證是否捕捉到 1618 (或週一回收車) 的請求
    has_1618 = any("run_id=1618" in u for u in recycle_schedule_requests)
    print("\n" + "="*50)
    if has_1618:
        print("🟢 戴明驗收 PASS：勾選雙收後，成功真實捕捉到 /schedule?run_id=1618 回收車請求！")
        sys.exit(0)
    else:
        print("❌ 戴明驗收 FAIL：未捕捉到 /schedule?run_id=1618 請求！")
        print("實際捕獲的請求：", recycle_schedule_requests)
        sys.exit(1)

finally:
    httpd.shutdown()
    httpd.server_close()
