#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/kage_tea_deep.py
====================================================================
🍵 atom-kage-clout-tea 萬用生活管家高情商走心對話與借光端茶引擎
首長：生活管家影 (Kage) ✕ 行銷長泰勒絲 (Taylor) ✕ 首席品質長戴明 (Dr. Deming)
具備四階端茶情境矩陣、零行銷推銷安燈閘門與全域萬用 JSON 輸出。
====================================================================
"""

import sys
import json
import argparse
import random
from typing import Dict, Any

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TEA_MODES = {
    "M1_TIRED": {
        "name": "深夜疲憊 / 打工辛勞 (Tired & Late Night)",
        "tone": "接住情緒、肯定付出、不談大道理",
        "templates": [
            "辛苦了，這個時間還亮著燈。今天已經很努力了，放下手機熱水泡個腳，早點休息。",
            "深夜的捷運車廂很空，心裡也很重吧。回到家先喝杯溫水，天大的事明天睡飽再說。",
            "看著你的字都感覺到肩膀的緊繃。給自己十分鐘深呼吸，今天你已經撐得很漂亮了。",
            "打工人的夜晚都是偷來的。別想工作了，熱個湯暖暖胃，今晚好好睡一覺。"
        ]
    },
    "M2_PRAISE": {
        "name": "鄰家好店 / 職人堅持 (Praise Artisan Detail)",
        "tone": "看懂細節、敬佩苦工、甘當綠葉",
        "templates": [
            "看這麵團的發酵氣孔就知道師傅起得有多早。巷弄裡有這份堅持，早晨變得特別踏實。",
            "真正的職人手藝都藏在別人看不見的死角。這份對細節的講究，懂的人一定會珍惜。",
            "每次看到你們家認真出菜的樣子，就覺得生活很有底氣。默默在角落為你們鼓掌。",
            "不需要大聲喧嘩，好東西自己會說話。謝謝你們把這份手作的溫度留給在地。"
        ]
    },
    "M3_WEATHER": {
        "name": "風雨天災 / 氣候居安 (Weather & Safety Care)",
        "tone": "實質關懷、溫柔叮嚀、家人守望",
        "templates": [
            "這波東北季風風勢不小，出門記得幫家裡長輩多帶件防風外套，門窗也順手扣緊喔。",
            "雨天視線差，路上機車特別多，騎慢一點不趕時間，平平安安到家才是第一名。",
            "天冷了，手腳容易冰涼。出門前喝口熱湯，把脖子圍好，照顧好自己比什麼都重要。",
            "風大雨大的日子，最幸福的就是家裡那盞暖黃色的燈。路上小心，慢行平安。"
        ]
    },
    "M4_HOMEY": {
        "name": "柴米油鹽 / 日常閒話 (Homey Warmth)",
        "tone": "平實共鳴、生活陪伴、煙火氣",
        "templates": [
            "家常菜再簡單，只要一家人圍著桌子熱騰騰地吃，這一天就圓滿及格了。",
            "生活就是由這些柴米油鹽的碎石子拼起來的。雖然瑣碎，但踩起來最踏實。",
            "聞到廚房煎魚的香味，就知道家的味道又回來了。平凡的日子，才是最珍貴的福氣。",
            "把今天的煩惱當成抹布，洗乾淨晾起來，明天太陽出來又是全新的一頁。"
        ]
    }
}

PROHIBITED_SALES_WORDS = [
    "點擊", "私訊", "下單", "推薦您", "優惠", "折扣", 
    "限時", "好康", "生活管家推薦", "極星", "買一送一", "立即購買"
]

def detect_tea_mode(text: str) -> str:
    """自動偵測對話情境"""
    t = text.lower()
    if any(k in t for k in ["累", "忙", "加班", "深夜", "下班", "捷運", "主管", "心累", "熬夜"]):
        return "M1_TIRED"
    elif any(k in t for k in ["堅持", "職人", "手作", "烘焙", "用心", "品質", "老店", "細節"]):
        return "M2_PRAISE"
    elif any(k in t for k in ["雨", "冷", "風", "降溫", "外套", "保暖", "颱風", "地震"]):
        return "M3_WEATHER"
    return "M4_HOMEY"

def audit_tea_etiquette(text: str) -> float:
    """戴明安燈端茶禮儀質檢 (滿分 100)"""
    score = 100.0
    for bad in PROHIBITED_SALES_WORDS:
        if bad in text:
            score -= 40.0 # 商業推銷嚴重扣分
    if len(text) < 20:
        score -= 20.0 # 太短顯得敷衍
    elif len(text) > 75:
        score -= 20.0 # 太長成了長篇說教
    return max(0.0, score)

def serve_tea(input_text: str, mode: str = None) -> Dict[str, Any]:
    """核心端茶話術生成器"""
    if not mode or mode not in TEA_MODES:
        mode = detect_tea_mode(input_text)
    
    cfg = TEA_MODES[mode]
    tea_speech = random.choice(cfg["templates"])
    score = audit_tea_etiquette(tea_speech)
    
    return {
        "status": "success",
        "mode": mode,
        "mode_name": cfg["name"],
        "tone_direction": cfg["tone"],
        "input_context": input_text,
        "tea_speech": tea_speech,
        "char_count": len(tea_speech),
        "etiquette_score": score,
        "poka_yoke_pass": score >= 90.0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-kage-clout-tea 萬用生活管家走心對話與借光端茶引擎")
    parser.add_argument("--input", type=str, default="忙到現在才把最後一份報表送出，捷運都快沒了", help="輸入情境文字或對方發言")
    parser.add_argument("--mode", type=str, default=None, choices=["M1_TIRED", "M2_PRAISE", "M3_WEATHER", "M4_HOMEY"], help="可選端茶模式")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = serve_tea(args.input, args.mode)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["tea_speech"])
    
    sys.exit(0)

if __name__ == "__main__":
    main()
