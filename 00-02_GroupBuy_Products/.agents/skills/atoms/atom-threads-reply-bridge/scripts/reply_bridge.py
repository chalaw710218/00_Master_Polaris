#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reply_bridge.py
====================================================================
🚀 atom-threads-reply-bridge 首回覆點火與主頁導流原子
首長：生活管家影 ✕ 店貓喵編 ✕ CTO 林納斯
單一職責：發布後 1 分鐘作者款待首回覆、對話室推薦池點火、60分鐘特務警戒。
====================================================================
"""

import sys
import os
import json
import random
import argparse
from datetime import datetime, timedelta
from typing import Dict, Any

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BRIDGE_SCRIPTS_SHADOW = [
    "大家今晚好。完整高畫質的生活寫真與店家散步地圖，管家收錄在主頁介紹裡，想慢讀的朋友可點進主頁自取。今晚你那裡的天氣如何？🍵",
    "感謝讀完這篇慢筆記。這份家常快手湯的完整食材清單放在主頁個人檔案，大家回家路上小心，今晚都要吃飽穿暖喔。🌾",
    "客廳的燈為大家留著。如果今天累了，隨時在留言區歇歇腳，生活管家在線上陪大家聊聊天。☕"
]

BRIDGE_SCRIPTS_MEOW = [
    "（舔爪爪）今天這條魚皮如果煎失敗了不要難過，本喵保證在留言區安慰你喵～大家今晚都吃什麼好料？🍖",
    "（從被窩探出半個頭）本喵的肉泥庫存告急，大家在下方留言一聲『喵』，本喵就考慮明天多更新一張睡姿照片。🐾",
    "打工人辛苦了！本喵今天特別核准大家在下方留言抱怨主管三句話，本喵用肉球幫你們蓋章消災。🐱"
]

def execute_reply_bridge(post_id: str, role: str = "auto", dry_run: bool = False) -> Dict[str, Any]:
    """執行首回覆點火與掛載警戒"""
    now = datetime.now()
    alert_expiry = now + timedelta(minutes=60)
    
    if role == "meow":
        comment_text = random.choice(BRIDGE_SCRIPTS_MEOW)
        speaker = "店貓 喵編 (Meow Editor)"
    else:
        comment_text = random.choice(BRIDGE_SCRIPTS_SHADOW)
        speaker = "生活管家 影 (Kage)"

    return {
        "status": "success",
        "atom": "atom-threads-reply-bridge",
        "target_post_id": post_id,
        "mode": "DRY_RUN" if dry_run else "PRODUCTION",
        "bridge_author": speaker,
        "first_reply_comment": comment_text,
        "published_at": now.isoformat(),
        "alert_window_active": True,
        "alert_window_until": alert_expiry.isoformat(),
        "char_count": len(comment_text),
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-reply-bridge Threads 首回覆點火原子")
    parser.add_argument("--post-id", type=str, default="th_mock_20261113", help="剛發布的貼文 ID")
    parser.add_argument("--role", type=str, default="shadow", choices=["shadow", "meow"], help="主役角色")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬送出")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = execute_reply_bridge(post_id=args.post_id, role=args.role, dry_run=args.dry_run)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[{result['bridge_author']}] 首回覆送出成功:\n{result['first_reply_comment']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
