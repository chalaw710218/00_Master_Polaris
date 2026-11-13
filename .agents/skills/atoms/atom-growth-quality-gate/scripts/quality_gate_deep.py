#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/quality_gate_deep.py
====================================================================
📐 atom-growth-quality-gate 萬用戴明五維品質出廠安燈閘門
首長：首席品質長戴明博士 (Dr. Deming) ✕ 法務長雪柔 (Falcon)
具備品牌法定紅線一票否決、反 AI 塑料感、常民共鳴與全域萬用出廠評定。
====================================================================
"""

import sys
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

# 品牌紅線詞（對外絕對不可出現）
BRAND_LEAK_WORDS = ["極星", "polaris", "POLARIS", "Polaris"]

# AI 腔與塑料套話黑名單
AI_PLASTIC_WORDS = [
    "親愛的", "探索", "引領", "助力", "賦能", "讓我們一起", 
    "在當今快節奏", "不容錯過", "璀璨", "點燃", "踏上旅程", "畫卷",
    "心動不如馬上行動", "福利來襲"
]

def audit_quality(text: str) -> Dict[str, Any]:
    """五維戴明安燈核心質檢函式"""
    text_clean = text.strip()
    
    # 1. 品牌紅線審查 (一票否決)
    for leak in BRAND_LEAK_WORDS:
        if leak in text:
            return {
                "status": "FAIL",
                "total_score": 0.0,
                "andon_light": "RED",
                "fatal_violation": f"觸犯品牌法定零洩漏紅線：偵測到內部代號【{leak}】！對外僅能稱『生活的一部分，就醬點！』或『生活管家』。",
                "feedback": "一票否決，立刻退回重修。",
                "exit_code": 0
            }

    # 2. 去 AI 塑料感評分 (25 分滿分)
    score_anti_ai = 25.0
    detected_plastics = []
    for plastic in AI_PLASTIC_WORDS:
        if plastic in text:
            score_anti_ai -= 6.0
            detected_plastics.append(plastic)
    score_anti_ai = max(0.0, score_anti_ai)

    # 3. 常民共鳴度 (25 分滿分)
    score_resonance = 20.0
    warm_cues = ["茶", "雨", "家", "生活", "累", "辛苦", "吃", "走", "看", "街", "貓", "台東"]
    if any(cue in text for cue in warm_cues):
        score_resonance += 5.0
    score_resonance = min(25.0, score_resonance)

    # 4. 留白與節奏感 (25 分滿分)
    score_pacing = 25.0
    if len(text_clean) > 280:
        score_pacing -= 8.0 # 文字壁扣分
    if "\n" not in text and len(text_clean) > 80:
        score_pacing -= 5.0 # 缺乏換行呼吸感

    # 5. 合規與真實度 (25 分滿分)
    score_safety = 25.0
    hype_words = ["保證治癒", "療效", "穩賺", "暴富", "100%保證"]
    for hw in hype_words:
        if hw in text:
            score_safety -= 15.0

    total_score = score_anti_ai + score_resonance + score_pacing + score_safety
    is_pass = total_score >= 88.0

    feedback_notes = []
    if detected_plastics:
        feedback_notes.append(f"偵測到 AI 塑料腔詞彙：{', '.join(detected_plastics)}")
    if total_score >= 90.0:
        feedback_notes.append("品質優良，市井煙火氣自然，符合出廠標準。")
    elif is_pass:
        feedback_notes.append("勉強達標，建議加強呼吸感與在地口語化。")
    else:
        feedback_notes.append("未達 88 分出廠門檻，需進一步去 AI 腔。")

    return {
        "status": "PASS" if is_pass else "FAIL",
        "total_score": round(total_score, 1),
        "andon_light": "GREEN" if is_pass else "YELLOW",
        "dimensions": {
            "anti_ai_tone": round(score_anti_ai * 4, 1),       # 換算為百分制
            "folk_resonance": round(score_resonance * 4, 1),
            "pacing_breath": round(score_pacing * 4, 1),
            "legal_safety": round(score_safety * 4, 1)
        },
        "feedback": "；".join(feedback_notes),
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-growth-quality-gate 萬用戴明五維品質出廠安燈閘門")
    parser.add_argument("--text", type=str, required=True, help="要質檢審查的文字內容")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = audit_quality(args.text)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[{result['andon_light']}] Score: {result['total_score']} - {result['status']}")
        print(result["feedback"])

    sys.exit(0)

if __name__ == "__main__":
    main()
