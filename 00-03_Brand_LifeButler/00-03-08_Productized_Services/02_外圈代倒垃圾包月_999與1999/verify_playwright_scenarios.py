# -*- coding: utf-8 -*-
"""
verify_playwright_scenarios.py
首席品質長 戴明 (Dr. Deming) 監製
嚴格比對三大驗收情境之【預期主答案 vs 雷達實際渲染結果】
以及生活圈按鈕狀態機驗收。
"""

import os
import sys
import io
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

PORT = 8095
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(CURRENT_DIR, "05_Trash_Radar_Engine")

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ENGINE_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def start_server():
    server = HTTPServer(("127.0.0.1", PORT), QuietHandler)
    server.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(1)

print("🚀 啟動 Playwright 實機嚴格驗收...")

# 定義三大情境
# 2026-11-17 是週二
# 2026-11-19 是週四
# 2026-11-16 是週一
SCENARIOS = [
    {
        "id": 1,
        "name": "驗收情境一（品碩重現條件）",
        "lat": 22.7594,
        "lon": 121.1400,
        "time_str": "2026-11-17T16:50:00+08:00", # 週二 16:50
        "day_desc": "週二 16:50",
        "expected_station": "新生路460號",
        "expected_plate": "KEH-5218",
        "expected_time": "16:54"
    },
    {
        "id": 2,
        "name": "驗收情境二（市區／正氣路水果街）",
        "lat": 22.7540,
        "lon": 121.1510,
        "time_str": "2026-11-19T17:15:00+08:00", # 週四 17:15
        "day_desc": "週四 17:15",
        "expected_station": "長沙街206巷口",
        "expected_plate": None,
        "expected_time": "17:20"
    },
    {
        "id": 3,
        "name": "驗收情境三（體育場）",
        "lat": 22.7523,
        "lon": 121.1465,
        "time_str": "2026-11-16T18:00:00+08:00", # 週一 18:00
        "day_desc": "週一 18:00",
        "expected_station": "洛陽街",
        "expected_plate": None,
        "expected_time": "18:02"
    }
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # 4. 驗收生活圈按鈕狀態機
    print("\n--------------------------------------------------")
    print("【小修驗收：生活圈按鈕狀態機】")
    context_fb = browser.new_context(viewport={"width": 430, "height": 932})
    page_fb = context_fb.new_page()
    page_fb.goto(f"http://127.0.0.1:{PORT}/index.html")
    page_fb.wait_for_selector("#btnHeroFind")

    # 檢查 1: 初始開啟時 #radarFallbackContainer 必須為 display: none
    fb_style_initial = page_fb.evaluate("() => window.getComputedStyle(document.getElementById('radarFallbackContainer')).display")
    print(f"1. 初始狀態 #radarFallbackContainer computed display: '{fb_style_initial}'")
    assert fb_style_initial == "none", f"Initial display must be none, got {fb_style_initial}"

    # 檢查 2: 點擊按鈕，模擬定位被拒絕
    # 透過未給權限或 mock navigator.geolocation.getCurrentPosition 失敗
    page_fb.evaluate("""() => {
        navigator.geolocation.getCurrentPosition = function(success, error) {
            setTimeout(() => {
                error({ code: 1, message: "User denied Geolocation" });
            }, 100);
        };
    }""")
    page_fb.click("#btnHeroFind")
    page_fb.wait_for_timeout(500)

    fb_style_denied = page_fb.evaluate("() => window.getComputedStyle(document.getElementById('radarFallbackContainer')).display")
    print(f"2. 定位拒絕後 #radarFallbackContainer computed display: '{fb_style_denied}'")
    assert fb_style_denied == "block", f"Denied display must be block, got {fb_style_denied}"
    print("✅ 生活圈按鈕狀態機驗收 PASS！")
    context_fb.close()

    # 檢驗三大情境
    print("\n--------------------------------------------------")
    print("【三大情境實機預期主答案 vs 雷達實際渲染結果比對】")

    for sc in SCENARIOS:
        print(f"\n▶ 執行 {sc['name']}：")
        print(f"   輸入條件：座標 ({sc['lat']}, {sc['lon']})，時間：{sc['day_desc']}")
        print(f"   預期主答案：目標站名「{sc['expected_station']}」（表定 {sc['expected_time']}）")

        context = browser.new_context(
            viewport={"width": 430, "height": 932},
            geolocation={"latitude": sc['lat'], "longitude": sc['lon']},
            permissions=["geolocation"]
        )

        # 注入時間 Mock
        time_iso = sc['time_str']
        init_js = f"""
            (function() {{
                const targetTime = new Date('{time_iso}');
                const OrigDate = window.Date;
                class FixedDate extends OrigDate {{
                    constructor(...args) {{
                        if (args.length === 0) {{
                            super(targetTime.getTime());
                        }} else {{
                            super(...args);
                        }}
                    }}
                    static now() {{
                        return targetTime.getTime();
                    }}
                }}
                window.Date = FixedDate;
            }})();
        """
        page = context.new_page()
        page.add_init_script(init_js)

        page.goto(f"http://127.0.0.1:{PORT}/index.html")
        page.wait_for_selector("#btnHeroFind")

        # 點擊「幫我找垃圾車」
        page.click("#btnHeroFind")

        # 等待渲染出主答案卡片
        try:
            page.wait_for_selector(".station-name", timeout=5000)
            actual_station = page.text_content(".station-name").strip()
        except Exception as e:
            actual_station = f"ERROR: 未渲染出 .station-name: {e}"

        # 讀取卡片內容確認抵達時間與車輛
        countdown_text = page.text_content(".primary-countdown").strip() if page.query_selector(".primary-countdown") else ""
        address_text = page.text_content(".station-address").strip() if page.query_selector(".station-address") else ""

        print(f"   雷達實際渲染站名：{actual_station}")
        print(f"   卡片倒數摘要：{countdown_text}")
        print(f"   卡片路線摘要：{address_text}")

        is_match = (actual_station == sc['expected_station'])
        status_str = "PASS (一致)" if is_match else "FAIL (不一致)"
        print(f"   判定結果：{status_str}")

        results.append({
            "id": sc['id'],
            "name": sc['name'],
            "coords": f"({sc['lat']}, {sc['lon']})",
            "time": sc['day_desc'],
            "expected_station": sc['expected_station'],
            "actual_station": actual_station,
            "match": is_match,
            "status": status_str,
            "countdown": countdown_text,
            "address": address_text
        })

        context.close()

    browser.close()

print("\n==================================================")
print("📊 戴明實機嚴格驗收總表：")
all_passed = True
for r in results:
    print(f"情境 {r['id']}: [{r['status']}] 預期「{r['expected_station']}」 vs 實際「{r['actual_station']}」")
    if not r['match']:
        all_passed = False

if all_passed:
    print("\n🎉 全部情境比對 100% 吻合！驗收通過！")
else:
    print("\n❌ 存在不一致情境！依品碩指示堅決判失敗！")
