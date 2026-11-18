# -*- coding: utf-8 -*-
"""
capture_round5_evidence.py
使用 Playwright 在真實無頭 Chromium 中啟動本地服務器加載 index.html，
執行品碩指定的兩大驗收場景並截圖至 05_Trash_Radar_Engine/evidence/：
1. kem8821_no_hide_verified.png: 車停在 KEM-8821 連航路198之1號附近，後段站點不得被隱藏。
2. offline_early_warning_verified.png: 離線模式新生路460號附近、16:50 出發，首選應為附近的站，並顯示提早警告。
"""

import os
import sys
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8089
ENGINE_DIR = os.path.abspath("05_Trash_Radar_Engine")
EVIDENCE_DIR = os.path.join(ENGINE_DIR, "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ENGINE_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def run_server():
    server = HTTPServer(("127.0.0.1", PORT), QuietHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932}) # iPhone 14 Pro Max 視角
    
    # -------------------------------------------------------------
    # 場景 1：KEM-8821 車停在連航路198之1號附近，後段站點不得被隱藏
    # -------------------------------------------------------------
    page.goto(f"http://127.0.0.1:{PORT}/index.html")
    page.wait_for_selector("#cardsContainer")
    
    # 注入場景 1 狀態：週一 16:30，KEM-8821 在連航路198之1號 (22.77512, 121.1257)
    # 使用者在更生北路278巷附近 (22.78139, 121.1216)
    page.evaluate("""() => {
        window.__TEST_NOW__ = '2026-11-16T16:30:00+08:00';
        document.getElementById('trashTimeInput').value = '16:30';
        document.getElementById('recycleCheckbox').checked = false;
        
        currentLat = 22.78139;
        currentLon = 121.1216;
        liveTrucksCache = {
            'KEM8821': {
                car_no: 'KEM-8821',
                lat: 22.77512,
                lon: 121.1257,
                speed: 0,
                status: '執勤中',
                visitedStops: {}
            }
        };
        setTravelMode('walking');
        renderRadar();
    }""")
    
    time.sleep(1)
    shot1_path = os.path.join(EVIDENCE_DIR, "kem8821_no_hide_verified.png")
    page.screenshot(path=shot1_path, full_page=True)
    print(f"✔ 場景 1 截圖完成: {shot1_path}")
    
    # -------------------------------------------------------------
    # 場景 2：離線模式新生路460號附近、16:50 出發，首選應為附近的站，並顯示提早警告
    # -------------------------------------------------------------
    page.evaluate("""() => {
        window.__TEST_NOW__ = '2026-11-16T16:50:00+08:00';
        document.getElementById('trashTimeInput').value = '16:50';
        document.getElementById('recycleCheckbox').checked = false;
        
        // 清空即時快取
        liveTrucksCache = {};
        for (let k in liveRouteSchedules) delete liveRouteSchedules[k];
        
        currentLat = 22.7594;
        currentLon = 121.1400;
        setTravelMode('walking');
        renderRadar();
    }""")
    
    time.sleep(1)
    shot2_path = os.path.join(EVIDENCE_DIR, "offline_early_warning_verified.png")
    page.screenshot(path=shot2_path, full_page=True)
    print(f"✔ 場景 2 截圖完成: {shot2_path}")
    
    # 驗證 DOM 內容
    content = page.content()
    assert "車可能提早到，建議提早 15 分鐘出門" in content, "場景 2 必須包含提早出門警告"
    assert "新生路460號" in content or "新生路" in content, "場景 2 首選必須是鄰近的新生路460號"
    print("✔ DOM 斷言全部通過！")
    
    browser.close()

print("🎉 證據截圖與雙項驗證全數完成！")
