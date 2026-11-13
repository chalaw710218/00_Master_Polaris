#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trio_crafter.py
====================================================================
🎭 atom-threads-trio-crafter 友店互動三風格走心擬稿工匠
首長：生活管家影 ✕ 店貓喵編 ✕ 行銷長泰勒絲
單一職責：三風格（溫暖/幽默/吃貨貓）走心擬稿、輸出 reply_to_id 即發 payload。
====================================================================
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, List

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def craft_trio_replies(post_id: str, text: str, handle: str = "") -> Dict[str, Any]:
    """生成三風格走心留言草稿"""
    t = text.lower()
    prefix = f"@{handle} " if handle else ""
    
    # 風格 1: 溫暖慢活 (影)
    if any(k in t for k in ["茶", "湯", "冷", "風", "熱"]):
        warm_speech = f"{prefix}台東這陣風真的吹得讓人直打哆嗦，看到你們這鍋熱氣騰騰的湯，整顆心都暖起來了。大家路上注意保暖呀！🍵"
    elif any(k in t for k in ["麵包", "烘焙", "酸種", "酵母"]):
        warm_speech = f"{prefix}看這發酵的氣孔就知道師傅清晨起了多大的早。能把手作的麥香留在台東街角，謝謝你們的用心堅持。🌾"
    else:
        warm_speech = f"{prefix}土地的餽贈最是真實。看著這份日常分享，生活管家也忍不住想把步調放慢，好好感受生活。✨"

    # 風格 2: 幽默鄰里 (影)
    if any(k in t for k in ["吃", "湯", "肉", "香"]):
        humor_speech = f"{prefix}這照片殺傷力太強了！管家剛剛才吃飽，看到這鍋又默默吞了兩口口水……可以幫我留一碗嗎？😋"
    else:
        humor_speech = f"{prefix}隔著螢幕都聞到香氣了，闆仔剛剛路過螢幕還以為是哪家大廚出巡呢！今天辛苦啦！🌿"

    # 風格 3: 傲嬌吃貨貓 (喵編)
    if any(k in t for k in ["肉", "骨", "魚", "吃", "香"]):
        meow_speech = f"{prefix}（動了動鼻子）本喵確認過香味了，這味道有合格。准你們現在送一碗過來給本喵驗收肉質！🐾"
    else:
        meow_speech = f"{prefix}（伸了個長長的懶腰）外面的風那麼大，本喵已經在被窩裡睡飽三個回合了，你們人類還在忙呀喵～🐱"

    drafts = [
        {
            "style_id": "STYLE_1_WARM",
            "author": "生活管家 影 (溫暖日常)",
            "reply_to_id": post_id,
            "text": warm_speech,
            "char_count": len(warm_speech)
        },
        {
            "style_id": "STYLE_2_HUMOR",
            "author": "生活管家 影 (幽默鄰里)",
            "reply_to_id": post_id,
            "text": humor_speech,
            "char_count": len(humor_speech)
        },
        {
            "style_id": "STYLE_3_MEOW",
            "author": "店貓 喵編 (傲嬌吃貨)",
            "reply_to_id": post_id,
            "text": meow_speech,
            "char_count": len(meow_speech)
        }
    ]

    return {
        "status": "success",
        "atom": "atom-threads-trio-crafter",
        "target_post_id": post_id,
        "input_snippet": text[:60] + "...",
        "drafts_count": len(drafts),
        "drafts": drafts,
        "ready_for_dispatch": True,
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-trio-crafter 友店互動三風格走心擬稿工匠")
    parser.add_argument("--post-id", type=str, default="th_post_hungry_088", help="友店貼文 ID")
    parser.add_argument("--text", type=str, default="今天台東風好大！我們連夜熬的大骨肉骨茶剛出爐，快來喝一碗避避風！", help="友店貼文文字")
    parser.add_argument("--handle", type=str, default="hungryyyummy", help="友店帳號")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = craft_trio_replies(post_id=args.post_id, text=args.text, handle=args.handle)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for d in result["drafts"]:
            print(f"[{d['author']}]:\n{d['text']}\n")

    sys.exit(0)

if __name__ == "__main__":
    main()
