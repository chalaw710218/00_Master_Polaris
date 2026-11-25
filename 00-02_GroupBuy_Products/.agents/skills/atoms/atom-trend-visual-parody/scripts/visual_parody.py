#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visual_parody.py
====================================================================
📸 atom-trend-visual-parody 熱點視覺微戲劇反差與便簽工匠原子
首長：首席視覺長約瑟夫 ✕ 店貓喵編 ✕ 行銷長泰勒絲
單一職責：35mm生活反差微戲劇提示詞、牛皮紙手寫便利貼微彩蛋設計。
====================================================================
"""

import sys
import os
import json
import argparse
from typing import Dict, Any

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PARODY_PRESETS = {
    "STOCK": {
        "scene": "股市震盪反差：金黃大雞腿便當死守戰",
        "prompt": "35mm analog photography, warm cozy indoor natural window lighting, a rustic wooden table with an authentic Taiwanese bento box featuring a huge golden crispy fried chicken leg and steaming hot rice. Beside the bento, a realistic domestic gray tabby cat with yellow-green eyes firmly places both front paws over the bento lid with an aloof, highly determined expression. In the blurred background, a laptop screen faintly reflects green chart lines, but the sharp focus is entirely on the juicy crispy fried chicken drumstick. Ultra-realistic food textures, gentle steam, cinematic grain, no digital smoothing.",
        "sticky_note": "2330 可以跌，但今天的大雞腿便當必須香！放過自己，好好吃肉。—— 生活管家"
    },
    "WEATHER": {
        "scene": "寒流強襲反差：滾沸剝皮辣椒雞湯與溫暖庇護",
        "prompt": "35mm documentary photography, cozy night kitchen atmosphere, rain droplets softly streaking across dark window panes in the background. On a sturdy weathered wooden dining table, a traditional clay pot is gently bubbling with rich amber broth, whole chicken, and green peeled chili peppers, soft steam rising. A steaming ceramic mug of hot ginger tea rests next to it. Soft golden warm overhead light, comforting domestic sanctuary feeling, deep organic shadows, warm grain.",
        "sticky_note": "外頭風大雨大，千萬別出門看浪。把這鍋熱湯喝透再睡！—— 生活管家 影"
    },
    "WORK": {
        "scene": "加班厭世/搶票塞爆反差：貓咪液態癱軟發呆",
        "prompt": "35mm candid slice-of-life photography, late afternoon domestic study room, a relaxed gray tabby cat completely liquefied, draping limply across a laptop keyboard with a totally blank, spaced-out stare. Beside the computer sits a thick slice of freshly toasted golden bread with butter melting in the center, and a glass of milk. Natural soft side light, authentic slightly messy desk, dust motes dancing in warm sunbeam, poetic imperfection.",
        "sticky_note": "連貓都累到融化了。工作先存檔，明天太陽出來再說！—— 生活管家"
    }
}

def generate_visual_parody(topic: str, category: str = "AUTO") -> Dict[str, Any]:
    """生成微戲劇提示詞與手寫便簽彩蛋"""
    cat = category.upper()
    if cat not in PARODY_PRESETS:
        t = topic.lower()
        if any(k in t for k in ["股", "2330", "跌", "漲", "錢", "幣"]):
            cat = "STOCK"
        elif any(k in t for k in ["天", "雨", "冷", "寒", "風", "降溫"]):
            cat = "WEATHER"
        else:
            cat = "WORK"

    config = PARODY_PRESETS[cat]

    return {
        "status": "success",
        "atom": "atom-trend-visual-parody",
        "topic": topic,
        "matched_category": cat,
        "parody_scene_concept": config["scene"],
        "visual_prompt_35mm": config["prompt"],
        "sticky_note_egg": {
            "text": config["sticky_note"],
            "material": "牛皮紙手寫便利貼 (Kraft Paper Sticky Note)",
            "placement": "便當盒邊緣或木桌前方顯眼角落",
            "dwell_time_boost": "引導讀者雙指放大細看，停留時間 (Dwell Time) 預估提升 150%"
        },
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-trend-visual-parody 熱點視覺微戲劇反差工匠原子")
    parser.add_argument("--topic", type=str, default="台積電盤面震盪大跌", help="時事話題")
    parser.add_argument("--category", type=str, default="AUTO", choices=["AUTO", "STOCK", "WEATHER", "WORK"], help="分類")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = generate_visual_parody(topic=args.topic, category=args.category)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[{result['parody_scene_concept']}]")
        print(f"便簽彩蛋: {result['sticky_note_egg']['text']}")
        print(f"35mm 提示詞:\n{result['visual_prompt_35mm']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
