#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試評估週三早晨喵編貼文
"""

import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from evaluate_threads_draft import evaluate_threads_draft

POST_TEXT = """週三早上九點二十分，看著人類背起公事包、邁著沉重腳步走出門
本喵已經在地板正中央的晨光裡打了三個滾，把灰色虎斑毛皮曬得暖烘烘喵🐾

抬頭看一下日曆！今天已經是週三小週末了！
一週最難熬的前半段已經被你甩在身後了，
如果現在走進辦公室覺得電量不足，
本喵允許你先隔空吸一口本喵被陽光曬暖的毛毛肚皮，滿血復活再出發喵～

大家今天早晨的第一杯飲料是黑咖啡、鮮奶茶，還是溫開水？喵🐾

#台東生活"""

score, report = evaluate_threads_draft(POST_TEXT)
print(f"得分: {score} / 100")
for r in report:
    print(f" - {r}")

if score < 90:
    sys.exit(1)
