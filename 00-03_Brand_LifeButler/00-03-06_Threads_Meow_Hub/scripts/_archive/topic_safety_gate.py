#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
topic_safety_gate.py — 社群熱門話題與政治敏感過濾硬門禁
落實鐵律 15（政治與對立絕對排除律）：生活管家不選邊站，嚴格排除政治、選舉、抗爭與黨派爭議話題。
"""

import re

# 政治敏感與爭議熱詞清單
POLITICAL_SENSITIVE_PATTERNS = [
    r"翡翠水庫",
    r"罷免",
    r"立法院",
    r"選戰",
    r"選舉",
    r"藍綠",
    r"政黨",
    r"立委",
    r"政治口水",
    r"國會改革",
    r"覆議案"
]

def check_topic_safety(text: str) -> tuple[bool, str]:
    """
    檢查主題是否觸犯政治爭議與敏感話題過濾門禁。
    回傳：(is_safe, reason)
    """
    if not text:
        return True, "內容為空"

    hit_words = []
    for pat in POLITICAL_SENSITIVE_PATTERNS:
        if re.search(pat, text):
            hit_words.append(pat)

    if hit_words:
        return False, f"【入庫拒絕】命中政治敏感與爭議話題過濾門禁（關鍵字：{', '.join(hit_words)}），依鐵律 15 堅決排除！"

    return True, "✅ 話題安全合格：未命中政治敏感關鍵字"

if __name__ == "__main__":
    t = "翡翠水庫爭議話題"
    ok, msg = check_topic_safety(t)
    print("Test:", ok, msg)
