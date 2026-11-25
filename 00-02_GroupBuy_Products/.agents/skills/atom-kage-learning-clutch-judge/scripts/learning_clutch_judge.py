#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
learning_clutch_judge.py - 影之脆自主學習離合器裁決引擎
版權所有 (c) 2026 極星內閣 - 首席特務兼生活管家影 (Kage)
"""

import sys
import json
import argparse
import re

# 強制 Windows 環境標準輸出採用 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 脆演算法有毒詞庫（絕對踩下離合器隔離）
TOXIC_NOISE_WORDS = [
    "我就問", "全台灣震驚", "網紅開撕", "政治立場", "對立", "公審", "炎上", "引戰",
    "保證發財", "獨家揭秘", "男女對立", "綠營", "藍營", "白營"
]

def judge_learning_clutch(data: dict) -> dict:
    """自主判定脆社群學習標的之離合器傳動狀態"""
    content = data.get("content", "")
    content_lower = content.lower()
    
    has_pol_bait = data.get("has_political_bait", False)
    has_gen_conflict = data.get("has_gender_conflict", False)
    has_authentic = data.get("has_authentic_lifestyle", False)
    
    # 1. 檢驗有毒雜訊
    toxic_hits = [w for w in TOXIC_NOISE_WORDS if w in content_lower]
    if has_pol_bait:
        toxic_hits.append("政治挑釁誘餌")
    if has_gen_conflict:
        toxic_hits.append("性別對立誘餌")
        
    if toxic_hits:
        clutch_state = "DISENGAGED (踩下離合器 · 斷開傳動)"
        directive = "❌ 絕不該學！此為脆演算法有毒死知識，踩下離合器空轉隔離，絕不污染影的心智！"
        action = "切斷學習神經鏈，後台靜默丟棄，嚴禁模仿"
    elif has_authentic or any(k in content for k in ["挖寶", "日常", "舊時光", "貓", "生活", "風土", "常民", "溫暖"]):
        clutch_state = "ENGAGED (全咬合 · 動力鎖定)"
        directive = "✅ 必須深學！具備強烈真實生活感與共鳴基因，全速傳動刻入突觸！"
        action = "提煉敘事鉤子與生活細節，刻入神經肌肉記憶，轉化為常態創作靈魂"
    else:
        clutch_state = "SLIPPING (半離合 · 緩衝試驗)"
        directive = "🟡 審慎觀察！具備潛在生活趣味，以 10% 算力進行單篇低成本微測試。"
        action = "納入待觀察試驗池，觀察脆友真實互動後再決定是否咬合"

    return {
        "content_snippet": content[:60] + ("..." if len(content) > 60 else ""),
        "clutch_state": clutch_state,
        "toxic_noise_detected": toxic_hits,
        "autonomous_learning_directive": directive,
        "action_protocol": action,
        "kage_reflection": "神經離合器裁決完畢！以真實生活為唯一北極星，守護創辦人生活主權！"
    }

def main():
    parser = argparse.ArgumentParser(description="影之脆自主學習離合器裁決引擎")
    parser.add_argument("--evaluate-topic", type=str, required=True, help="受檢社群貼文或話題 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.evaluate_topic)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = judge_learning_clutch(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
