#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tea_funnel.py
====================================================================
🍵 atom-threads-tea-funnel Threads 公域借光端茶與獲客引流原子
首長：生活管家影 ✕ 店貓喵編 ✕ CTO 林納斯
單一職責：公域熱門焦慮大串反差體溫端茶、真貓解構、優雅獲客引流。
====================================================================
"""

import sys
import os
import json
import random
import argparse
from typing import Dict, Any

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TEA_SCRIPTS_SHADOW = [
    "看大家衝流量衝得這麼認真，生活管家默默在後排切了一盤剛熟好的台東大目釋迦... 大家先喝口熱茶順順氣。衝演算法的同時，今晚的胃還是需要一碗熱湯撫慰呀。🍵",
    "加班辛苦了。深夜的都市雖然喧鬧，但家裡總該有一盞留給自己的暖燈。路上騎車慢一點，深呼吸，今天你已經做得夠好了。🌾",
    "大家都在算如何破圈，管家只想提醒大家別忘了按時吃飯。這鍋剝皮辣椒雞湯剛熄火，把這份熱氣留給正在滑手機的你。🍲"
]

TEA_SCRIPTS_MEOW = [
    "（從紙箱探頭）喵... 你們人類一天到晚算流量密碼不累嗎？本喵的密碼只有一個：就是人類煎蛋時掉在桌上的那一小塊蛋白。🐾",
    "（一腳踩在鍵盤上）那麼焦慮幹嘛？天塌下來先抓抓貓抓板，反正你也解決不了。過來摸兩把冷靜一下吧愚蠢的人類。🐱",
    "看你們打字打得手指都要抽筋了。本喵已經睡了三個回合，奉勸大家現在立刻關螢幕去翻冰箱。🐟"
]

PROHIBITED_POISON = ["+1", "互追", "求回追", "點擊連結", "主頁有賣", "買一送一", "生活管家推薦您", "極星"]

def generate_tea_comment(topic: str, role: str = "auto") -> Dict[str, Any]:
    """生成反差體溫借光端茶評論"""
    if role == "auto":
        role = "meow" if random.random() < 0.4 else "shadow"
        
    if role == "meow":
        speech = random.choice(TEA_SCRIPTS_MEOW)
        speaker = "店貓 喵編 (Meow Editor)"
    else:
        speech = random.choice(TEA_SCRIPTS_SHADOW)
        speaker = "生活管家 影 (Kage)"
        
    # 安全安燈審查
    for bad in PROHIBITED_POISON:
        if bad in speech:
            speech = speech.replace(bad, "")

    return {
        "status": "success",
        "atom": "atom-threads-tea-funnel",
        "target_topic": topic,
        "role": speaker,
        "clout_tea_speech": speech,
        "char_count": len(speech),
        "anti_algorithm_poison": True,
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-tea-funnel Threads 公域借光端茶原子")
    parser.add_argument("--topic", type=str, default="自媒體焦慮與加班", help="公域大串主題")
    parser.add_argument("--role", type=str, default="auto", choices=["auto", "shadow", "meow"], help="端茶角色")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = generate_tea_comment(topic=args.topic, role=args.role)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[{result['role']}] 端茶話術:\n{result['clout_tea_speech']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
