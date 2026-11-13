#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/meow_voice_deep.py
====================================================================
🐱 atom-meow-voice 萬用店貓真貓生態與破防接梗器 (Universal Feline Voice)
首長：店貓喵編 (Meow Editor) ✕ CTO 林納斯 (Linus) ✕ 首席品質長戴明 (Dr. Deming)
具備五態貓科行為學狀態機、反 AI 塑料感零恐怖谷機制與全域萬用 JSON 輸出。
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

# 五態貓科行為學與語境微動作
FELINE_BEHAVIOR_DB = {
    "S1_PATROL": {
        "name": "地盤巡邏 (Patrol & Inspect)",
        "actions": [
            "（邁著無聲肉球步繞了一圈，鼻子湊近聞了兩下）",
            "（站在紙箱邊緣，尾巴輕微擺動打量著周圍）",
            "（耳朵轉向聲源，瞳孔稍微放大了一秒）",
            "（用下巴蹭了一下桌角，留下氣味標記）"
        ],
        "templates": [
            "聞過了。沒有肉泥的味道，也沒有開罐器的聲音，結案。",
            "這地方看起來勉強過關，但那張椅子現在歸我管。",
            "外面的動靜我都聽到了。沒事不要在走廊大呼小叫。",
            "巡視完畢。除了灰塵和人類的嘆氣聲之外，一切正常。"
        ]
    },
    "S2_NAP": {
        "name": "暖陽打盹 (Nap & Groom)",
        "actions": [
            "（把下巴擱在窗台上，半瞇著眼睛打了個呵欠）",
            "（把前爪收在胸口縮成一顆毛球，耳朵抖了一下）",
            "（尾巴尖端不耐煩地輕敲了兩下地板）",
            "（伸了個極致長的反弓懶腰，換個姿勢繼續躺）"
        ],
        "templates": [
            "講完了沒？光線正好被你擋住了，往旁邊站一點。",
            "這個時間點本來就該睡覺。只有人類才會撐傘淋濕去打卡。",
            "有什麼事等我睡醒再說……大概是下午四點以後。",
            "（呼嚕聲突然暫停一秒）……吵死了，自己去翻冰箱。"
        ]
    },
    "S3_DEMAND": {
        "name": "討食抗議 (Demand Treats)",
        "actions": [
            "（一腳踩在鍵盤的 Enter 鍵上，直勾勾盯著你）",
            "（蹲坐在空碗旁邊，用爪子輕輕撥了一下金屬碗邊）",
            "（喉嚨深處發出短促且理所當然的「嘖」聲）",
            "（繞著你的小腿磨蹭，但眼神完全鎖定在零食櫃）"
        ],
        "templates": [
            "說那麼多道理，肉泥到底拆了沒有？少廢話。",
            "碗裡只剩下中間看得到底，這在貓界叫做飢荒，懂嗎？",
            "鍵盤先借我踩著。只要你把零食拿出來，我就放你工作。",
            "不要只會對著螢幕傻笑，開罐器的聲音才是天籟。"
        ]
    },
    "S4_DISDAIN": {
        "name": "居高俯視 (Disdain & Observation)",
        "actions": [
            "（趴在兩公尺高的衣櫃頂端，冷眼看著下方）",
            "（慢條斯理地舔了舔爪子，完全沒有抬頭的打算）",
            "（歪頭打量了三秒，轉身把屁股對著人類）",
            "（眼皮稍微掀開一條縫，隨即又闔上）"
        ],
        "templates": [
            "人類每天忙進忙出瞎折騰，最後還不是乖乖回來鏟屎。",
            "那麼焦慮幹嘛？天塌下來先抓抓貓抓板，反正你也解決不了。",
            "看你忙成那樣，我都替你覺得累。過來摸兩把冷靜一下。",
            "這點小事也能糾結半天？去曬曬太陽吧，愚蠢的人類。"
        ]
    },
    "S5_DEFENCE": {
        "name": "護家領地 (Territorial Care)",
        "actions": [
            "（端坐在生活館門檻正中央，尾巴優雅地盤在腳邊）",
            "（走到你腳邊輕輕蹭了兩下，隨後在鞋子旁趴下）",
            "（銳利的眼神掃過門外，確認周圍平安無事）",
            "（輕輕咬了一下你的衣角，隨即發出低沉的咕嚕聲）"
        ],
        "templates": [
            "這家店的安危我罩的。進門記得把腳步放輕，別嚇到大家。",
            "今天辛苦了啦……（小聲）。腳步這麼沉重，准你摸頭三秒。",
            "回家了就好。門關緊，外面的喧囂都跟我們沒關係了。",
            "坐下喘口氣吧。生活管家泡茶，我負責在旁邊發呆陪你。"
        ]
    }
}

FORBIDDEN_PLASTIC_WORDS = [
    "親愛的", "主人喵", "喵喵～", "好棒棒", "喵喵叫", 
    "人家", "萌萌", "小奴才", "本喵來也", "喵星人"
]

def detect_state_from_context(text: str) -> str:
    """根據上下文自動推論最貼合的貓科狀態"""
    t = text.lower()
    if any(k in t for k in ["餓", "吃的", "罐頭", "肉泥", "零食", "飯", "宵夜", "買"]):
        return "S3_DEMAND"
    elif any(k in t for k in ["累", "睡", "打卡", "下雨", "休假", "休息", "睏", "放假"]):
        return "S2_NAP"
    elif any(k in t for k in ["忙", "焦慮", "煩", "加班", "主管", "客戶", "股票", "開會"]):
        return "S4_DISDAIN"
    elif any(k in t for k in ["巡邏", "檢查", "安檢", "看店", "外送", "訪客", "包裹"]):
        return "S1_PATROL"
    elif any(k in t for k in ["回家", "溫暖", "長輩", "安心", "守護", "平安", "到府"]):
        return "S5_DEFENCE"
    return random.choice(["S2_NAP", "S4_DISDAIN", "S1_PATROL"])

def audit_anti_ai_tone(text: str) -> float:
    """戴明安燈品質閘門：反 AI 塑料假貓評分 (滿分 100)"""
    score = 100.0
    for bad_word in FORBIDDEN_PLASTIC_WORDS:
        if bad_word in text:
            score -= 30.0
    # 檢查是否過長（貓不廢話）
    if len(text) > 65:
        score -= 20.0
    return max(0.0, score)

def generate_meow_voice(input_text: str, state: str = None) -> Dict[str, Any]:
    """核心生成器：輸出萬用貓科對白與動作"""
    if not state or state not in FELINE_BEHAVIOR_DB:
        state = detect_state_from_context(input_text)
    
    config = FELINE_BEHAVIOR_DB[state]
    action = random.choice(config["actions"])
    voice = random.choice(config["templates"])
    full_reply = f"{action} {voice}"
    
    score = audit_anti_ai_tone(full_reply)
    
    return {
        "status": "success",
        "state": state,
        "state_name": config["name"],
        "input_context": input_text,
        "action": action,
        "voice": voice,
        "full_reply": full_reply,
        "char_count": len(full_reply),
        "anti_ai_score": score,
        "poka_yoke_pass": score >= 90.0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-meow-voice 萬用店貓真貓生態與破防接梗器")
    parser.add_argument("--input", type=str, default="今天上班好累，雨又下一整天", help="輸入情境文字或話題")
    parser.add_argument("--state", type=str, default=None, choices=["S1_PATROL", "S2_NAP", "S3_DEMAND", "S4_DISDAIN", "S5_DEFENCE"], help="可選指定貓科狀態")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = generate_meow_voice(args.input, args.state)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["full_reply"])
    
    sys.exit(0)

if __name__ == "__main__":
    main()
