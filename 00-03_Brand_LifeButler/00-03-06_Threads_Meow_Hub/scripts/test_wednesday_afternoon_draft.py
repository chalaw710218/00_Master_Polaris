#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試評估週三下午喵編貼文
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

POST_TEXT = """週三下午三點十五分，看著人類眼神渙散、滑鼠滾輪漫無目的地上下滾動
本喵早就把下巴舒服地貼在溫熱的木桌上，準備啟動午後第二輪深層充電模式了喵🐾

再撐一下！週三下午一過，週末就已經在向你揮手了！
如果現在眼皮重得像掛了鉛塊，
本喵允許你先隔空吸一口本喵毛茸茸的灰色虎斑小腦袋充電喵～

大家現在是在偷偷看下班吃什麼，還是在猛灌冰美式續命？喵🐾

#台東生活"""

score, report = evaluate_threads_draft(POST_TEXT)
print(f"得分: {score} / 100")
for r in report:
    print(f" - {r}")

if score < 90:
    sys.exit(1)
