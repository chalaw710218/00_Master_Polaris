# -*- coding: utf-8 -*-
import sys
import io
import urllib.request
import urllib.parse
import json

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# 查詢政府資料開放平台 (data.gov.tw) 或環境部清運車輛資料
# API: 垃圾清運車輛軌跡 / 清運路線
endpoints = [
    "https://data.moenv.gov.tw/api/v2/gp_p_01?api_key=test&limit=10",
    "https://cleanbus.moenv.gov.tw",
]

# 我們先搜尋 web 關於 台東市 清運E點通 車牌 或 興航街 清運車號
print("Checking keywords...")
