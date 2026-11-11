# -*- coding: utf-8 -*-
import sys
import io
import urllib.request
import json

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# 檢查 probe_cleanbus_api.py 的內容
with open('05_Trash_Radar_Engine/probe_cleanbus_api.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:60]):
    print(f"{i+1}: {l.strip()}")
