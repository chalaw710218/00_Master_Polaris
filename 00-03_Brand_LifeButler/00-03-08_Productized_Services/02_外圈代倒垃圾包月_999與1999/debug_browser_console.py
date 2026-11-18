# -*- coding: utf-8 -*-
import http.server
import socketserver
import threading
import time
from playwright.sync_api import sync_playwright

PORT = 8767
httpd = socketserver.TCPServer(('127.0.0.1', PORT), http.server.SimpleHTTPRequestHandler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on('console', lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
    page.on('pageerror', lambda err: print(f"PAGEERROR: {err}"))
    page.on('request', lambda r: print(f"REQUEST: {r.method} {r.url}") if "/schedule" in r.url else None)
    
    page.add_init_script("window.__TEST_NOW__ = '2026-11-16T17:00:00+08:00';")
    print("Loading page...")
    page.goto(f'http://127.0.0.1:{PORT}/05_Trash_Radar_Engine/index.html')
    time.sleep(3)
    
    print("\nClicking #recycleBox...")
    page.click("#recycleBox")
    time.sleep(3)
    
    browser.close()
