#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 80/20 廣域漏斗社交巡邏機 (Threads 80/20 Broad-Reach Social Funnel)
依據創辦人親定哲學：10個人接觸、8個人點愛心留足跡、2個人深度走心互動。
從 following_targets.json 的 185 家台東在地店家與創作者中動態選取，全域擴大接觸面。
作者: 影 (Shadow)
"""

import os
import sys
import json
import time
import random
from pathlib import Path

# 確保 Windows 支援 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
TARGETS_FILE = SCRIPT_DIR / "following_targets.json"
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
SCREENSHOT_DIR = SCRIPT_DIR / "screenshots"

def load_diverse_targets(count=10):
    """從 185 家目標庫中隨機跨類別抽取 10 個不重複帳號"""
    if not TARGETS_FILE.exists():
        return []

    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = data.get("categories", {})
    all_targets = []
    for cat_name, items in categories.items():
        for item in items:
            uname = item.get("username", "").strip()
            # 排除已過期或被凍結的慢食節
            if uname and "..." not in uname and uname != "slowfoodtaitung":
                all_targets.append({
                    "username": uname,
                    "name": item.get("name", uname),
                    "category": cat_name
                })

    random.shuffle(all_targets)
    return all_targets[:count]

if __name__ == "__main__":
    targets = load_diverse_targets(10)
    print(f"🎯 [80/20 廣域漏斗] 本次隨機抽取 10 位在地店家與創作者:")
    for idx, t in enumerate(targets, 1):
        print(f"  {idx}. @{t['username']}（{t['name']}）- 領域: {t['category']}")
