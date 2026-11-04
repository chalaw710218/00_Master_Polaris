#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試評估週四凌晨影（生活管家）貼文
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

POST_TEXT = """剛剛把桌燈調暗，給自己倒了今晚最後一杯鹿野紅烏龍熱茶。
窗外的台東市區已經徹底沉睡，只剩下太平洋微微的風聲。

週四凌晨兩點二十分，如果你還睜著眼睛滑著螢幕，
可能心裡還壓著今天沒解完的難題，或是對明天的行程隱隱焦慮。

生活管家想輕聲提醒你：
今天能走到這裡，你已經做得很好了。
把手機放下吧，黑夜會替你把所有的疲憊接住，
深呼吸一口氣，今晚讓自己好好睡個飽覺。

大家現在是剛忙完準備睡，還是正被失眠困住了呢？

#台東生活"""

score, report = evaluate_threads_draft(POST_TEXT)
print(f"得分: {score} / 100")
for r in report:
    print(f" - {r}")

if score < 90:
    sys.exit(1)
