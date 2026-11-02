#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試評估週一深夜喵編貼文
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

POST_TEXT = """週一深夜十一點半，看著人類終於洗完澡、把筆電闔上、嘆了今天最後一口氣
本喵早就把身體蜷成一個暖呼呼的灰色虎斑毛球，在棉被正中間卡好位了喵🐾

辛苦了，最難熬的週一已經被你徹底解決掉了！
今晚就別再滑手機回顧明天的待辦清單了，
趕快鑽進被窩，把冰冰的腳伸到本喵肚子底下取暖吧喵～

大家今晚的被窩夠暖嗎？睡前要記得喝口溫水喵🐾

#台東生活"""

score, report = evaluate_threads_draft(POST_TEXT)
print(f"得分: {score} / 100")
for r in report:
    print(f" - {r}")

if score < 90:
    sys.exit(1)
