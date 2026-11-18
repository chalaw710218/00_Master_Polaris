# -*- coding: utf-8 -*-
"""
generate_all_evidence_screenshots.py
首席品質長 戴明 (Dr. Deming) 監製
台東垃圾車即時雷達全新規範 (Josef ✕ Neo ✕ Linus)
100% 真實執行流程 5 大驗收畫面實機截圖存證

1. 01_initial_clean_screen.png: 剛打開純大按鈕空白首屏（乾淨一屏，無卡片、無定位彈窗）
2. 02_locating_searching_state.png: 點擊按鈕後的定位中狀態（按鈕文字顯示「📡 定位中…」，disabled）
3. 03_master_answer_active.png: 出勤主答案（真實注入情境一：週二 16:50 新生路460號，真實運算渲染主答案卡片）
4. 04_after_hours_with_butler.png: 收工預報+代倒（真實注入深夜 22:30，觸發今日已收工5筆預報 ＋ 生活管家 999/1999 包月服務卡）
5. 05_fallback_zones_prompt.png: 拒絕定位生活圈（真實模擬拒絕定位，狀態機切換至 display: block 展開 8 大生活圈兜底按鈕）
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

PORT = 8097
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(CURRENT_DIR, "05_Trash_Radar_Engine")
EVIDENCE_DIR = os.path.join(ENGINE_DIR, "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

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

print("🚀 啟動 Playwright 實機截圖存證...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # 畫面 1: 01_initial_clean_screen.png
    print("📸 擷取畫面 1: 剛打開純大按鈕空白首屏...")
    ctx1 = browser.new_context(viewport={"width": 430, "height": 932})
    page1 = ctx1.new_page()
    page1.goto(f"http://127.0.0.1:{PORT}/index.html")
    page1.wait_for_selector("#btnHeroFind")
    time.sleep(0.5)
    shot1_path = os.path.join(EVIDENCE_DIR, "01_initial_clean_screen.png")
    page1.screenshot(path=shot1_path, full_page=False)
    print(f"✔ [1/5] 已存檔: {shot1_path}")
    ctx1.close()

    # 畫面 2: 02_locating_searching_state.png
    print("📸 擷取畫面 2: 定位中處理狀態...")
    ctx2 = browser.new_context(viewport={"width": 430, "height": 932})
    page2 = ctx2.new_page()
    page2.add_init_script("""
        navigator.geolocation.getCurrentPosition = function(success, error) {
            // 刻意延遲回調，保持定位中狀態供截圖
        };
    """)
    page2.goto(f"http://127.0.0.1:{PORT}/index.html")
    page2.wait_for_selector("#btnHeroFind")
    page2.click("#btnHeroFind")
    time.sleep(0.4)
    shot2_path = os.path.join(EVIDENCE_DIR, "02_locating_searching_state.png")
    page2.screenshot(path=shot2_path, full_page=False)
    print(f"✔ [2/5] 已存檔: {shot2_path}")
    ctx2.close()

    # 畫面 3: 03_master_answer_active.png
    print("📸 擷取畫面 3: 出勤主答案真實渲染 (情境一：週二 16:50 新生路460號)...")
    ctx3 = browser.new_context(
        viewport={"width": 430, "height": 932},
        geolocation={"latitude": 22.7594, "longitude": 121.1400},
        permissions=["geolocation"]
    )
    ctx3.add_init_script("""
        (function() {
            const targetTime = new Date('2026-11-17T16:50:00+08:00');
            const OrigDate = window.Date;
            class FixedDate extends OrigDate {
                constructor(...args) {
                    if (args.length === 0) super(targetTime.getTime());
                    else super(...args);
                }
                static now() { return targetTime.getTime(); }
            }
            window.Date = FixedDate;
        })();
    """)
    page3 = ctx3.new_page()
    page3.goto(f"http://127.0.0.1:{PORT}/index.html")
    page3.wait_for_selector("#btnHeroFind")
    page3.click("#btnHeroFind")
    page3.wait_for_selector(".station-name", timeout=5000)
    time.sleep(0.5)
    shot3_path = os.path.join(EVIDENCE_DIR, "03_master_answer_active.png")
    page3.screenshot(path=shot3_path, full_page=True)
    print(f"✔ [3/5] 已存檔: {shot3_path}")
    ctx3.close()

    # 畫面 4: 04_after_hours_with_butler.png
    print("📸 擷取畫面 4: 收工預報+代倒真實渲染 (深夜 22:30)...")
    ctx4 = browser.new_context(
        viewport={"width": 430, "height": 932},
        geolocation={"latitude": 22.7554, "longitude": 121.1505},
        permissions=["geolocation"]
    )
    ctx4.add_init_script("""
        (function() {
            const targetTime = new Date('2026-11-17T22:30:00+08:00');
            const OrigDate = window.Date;
            class FixedDate extends OrigDate {
                constructor(...args) {
                    if (args.length === 0) super(targetTime.getTime());
                    else super(...args);
                }
                static now() { return targetTime.getTime(); }
            }
            window.Date = FixedDate;
        })();
    """)
    page4 = ctx4.new_page()
    page4.goto(f"http://127.0.0.1:{PORT}/index.html")
    page4.wait_for_selector("#btnHeroFind")
    page4.click("#btnHeroFind")
    page4.wait_for_selector(".eod-card", timeout=5000)
    time.sleep(0.5)
    shot4_path = os.path.join(EVIDENCE_DIR, "04_after_hours_with_butler.png")
    page4.screenshot(path=shot4_path, full_page=True)
    print(f"✔ [4/5] 已存檔: {shot4_path}")
    ctx4.close()

    # 畫面 5: 05_fallback_zones_prompt.png
    print("📸 擷取畫面 5: 拒絕定位生活圈兜底按鈕區...")
    ctx5 = browser.new_context(viewport={"width": 430, "height": 932})
    ctx5.add_init_script("""
        navigator.geolocation.getCurrentPosition = function(success, error) {
            setTimeout(() => {
                error({ code: 1, message: "User denied Geolocation" });
            }, 100);
        };
    """)
    page5 = ctx5.new_page()
    page5.goto(f"http://127.0.0.1:{PORT}/index.html")
    page5.wait_for_selector("#btnHeroFind")
    page5.click("#btnHeroFind")
    page5.wait_for_selector(".district-fallback-matrix", timeout=5000)
    time.sleep(0.5)
    shot5_path = os.path.join(EVIDENCE_DIR, "05_fallback_zones_prompt.png")
    page5.screenshot(path=shot5_path, full_page=True)
    print(f"✔ [5/5] 已存檔: {shot5_path}")
    ctx5.close()

    browser.close()

print("\n🎉 5 大真實實機驗收截圖全數更新完畢！")
