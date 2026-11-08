#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生活管家・一鍵倒垃圾雷達 本地預覽伺服器
由工程長 林納斯 (Linus) 監製
支援電腦本機 (localhost) 與 手機同 Wi-Fi (LAN IP) 雙軌預覽
"""

import http.server
import socketserver
import os
import sys
import io
import socket

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # 保持日誌乾淨
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    local_ip = get_local_ip()
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("==================================================")
        print("🚀 生活管家・一鍵倒垃圾雷達 本地預覽伺服器已啟動！")
        print("==================================================")
        print(f"💻 電腦瀏覽請開啟： http://localhost:{PORT}/index.html")
        print(f"📱 手機 (同Wi-Fi) 請開啟： http://{local_ip}:{PORT}/index.html")
        print("==================================================")
        print("按 Ctrl+C 可停止伺服器。")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n預覽伺服器已正常停止。")
