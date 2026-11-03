#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試評估週二下午喵編貼文
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

POST_TEXT = """週二下午三點十五分，看著人類盯著試算表哈欠連連
本喵剛在溫暖的木頭窗邊伸完一個超長大懶腰，把前腳拉得筆直喵🐾

撐住！最漫長的前兩天就快熬過一半了！
如果現在咖啡因已經失效、眼皮沉到快閉起來，
本喵特准你把視線移到本喵發亮的灰色虎斑毛皮上，隔空吸飽電再繼續奮鬥喵～

大家現在手邊端著的是手搖飲、美式，還是已經想趴下睡十分鐘了？喵🐾

#台東生活"""

score, report = evaluate_threads_draft(POST_TEXT)
print(f"得分: {score} / 100")
for r in report:
    print(f" - {r}")

if score < 90:
    sys.exit(1)
