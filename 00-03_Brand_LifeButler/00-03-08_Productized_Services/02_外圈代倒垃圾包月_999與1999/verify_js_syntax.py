# -*- coding: utf-8 -*-
import sys
import re
import subprocess
import os

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

INDEX_PATH = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-08_Productized_Services\02_外圈代倒垃圾包月_999與1999\05_Trash_Radar_Engine\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

scripts = re.findall(r"<script(?:\s+[^>]*)?>(.*?)</script>", html, re.DOTALL)
print(f"Found {len(scripts)} script tags")

# 檢查最大的主程式 script
main_js = scripts[-1]
temp_js_path = "temp_check.js"
with open(temp_js_path, "w", encoding="utf-8") as f:
    f.write(main_js)

try:
    res = subprocess.run(["node", "--check", temp_js_path], capture_output=True, text=True)
    if res.returncode == 0:
        print("PASS: JavaScript syntax AST check 100% PASSED (node --check exit code: 0)!")
    else:
        print("FAIL: JavaScript syntax ERROR:")
        print(res.stderr)
        exit(1)
finally:
    if os.path.exists(temp_js_path):
        os.remove(temp_js_path)
