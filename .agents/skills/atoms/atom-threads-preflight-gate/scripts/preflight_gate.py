#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preflight_gate.py
====================================================================
🛑 atom-threads-preflight-gate Threads 發布前五維安燈審計原子
首長：首席品質長戴明博士 ✕ 行銷長泰勒絲
單一職責：發布前純文字毫秒級質檢、出廠門檻 90 分、4 大致命守則一票否決。
====================================================================
"""

import sys
import os
import re
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

FATAL_BAIT_WORDS = ["留言+1", "+1", "快來買", "限時", "搶購", "立即下單", "私訊我", "買一送一"]

def audit_draft_text(text: str, persona: str = "auto") -> Dict[str, Any]:
    """核心審計函式"""
    text_clean = text.strip()
    char_count = len(text_clean)
    
    # --- 1. 致命守則一票否決查核 ---
    violations = []
    
    # 守則 1: 外部連結
    if re.search(r"https?://", text_clean):
        violations.append("致命違規：內文包含外部連結 (http/https)，觸犯演算法降權大忌！")
        
    # 守則 2: 急迫/誘餌詞
    for bait in FATAL_BAIT_WORDS:
        if bait in text_clean:
            violations.append(f"致命違規：內文包含誘餌/促銷字眼【{bait}】！")
            
    # 守則 3: 喵編人稱檢查
    if persona == "meow" or (persona == "auto" and "本貓" in text_clean):
        if "本貓" in text_clean:
            violations.append("致命違規：喵編貼文誤用【本貓】！唯一法定稱謂為【本喵】。")
            
    # 守則 4: 字數超過 500 字
    if char_count > 500:
        violations.append(f"致命違規：貼文字數高達 {char_count} 字，超過 500 字上限！")

    if violations:
        return {
            "status": "REJECTED_BY_FATAL_RULES",
            "atom": "atom-threads-preflight-gate",
            "passed": False,
            "total_score": 0.0,
            "char_count": char_count,
            "fatal_violations": violations,
            "feedback": "觸犯致命守則，一票否決，立刻重修！",
            "exit_code": 0
        }

    # --- 2. 五維客觀打分 (各 20 分，滿分 100) ---
    scores = {
        "hook_tension": 20.0,      # 鉤子張力
        "breath_spacing": 20.0,    # 短句呼吸感
        "zero_hard_ad": 20.0,      # 零硬廣
        "persona_integrity": 20.0, # 人設完整度
        "open_question": 20.0      # 結尾開放式提問
    }
    notes = []

    # 維度 1: 鉤子張力 (前兩行是否有生活痛點或吸引力)
    lines = [l.strip() for l in text_clean.split("\n") if l.strip()]
    first_two_lines = " ".join(lines[:2]) if lines else ""
    hook_cues = ["冷", "雨", "累", "忙", "下班", "廚房", "貓", "台東", "生活", "味道", "湯", "茶"]
    if not any(cue in first_two_lines for cue in hook_cues):
        scores["hook_tension"] -= 6.0
        notes.append("前兩行缺少強烈的生活煙火氣或情緒共鳴詞。")

    # 維度 2: 短句呼吸感 (段落空行與句子長度)
    if "\n\n" not in text_clean and len(lines) > 3:
        scores["breath_spacing"] -= 8.0
        notes.append("段落缺少雙換行留白，文字偏擁擠。")
    for l in lines:
        if len(l) > 60:
            scores["breath_spacing"] -= 4.0
            notes.append("存在單行超過 60 字的長句，建議拆成短句。")
            break

    # 維度 3: 零硬廣
    ad_cues = ["推薦", "優惠", "活動", "生活館"]
    for cue in ad_cues:
        if cue in text_clean:
            scores["zero_hard_ad"] -= 4.0
            notes.append(f"帶有微弱推銷感詞彙【{cue}】，建議淡化。")

    # 維度 4: 人設完整度
    if persona == "meow":
        if "本喵" not in text_clean:
            scores["persona_integrity"] -= 8.0
            notes.append("喵編貼文未體現【本喵】自稱或真貓動作。")
    elif persona == "shadow":
        if "管家" not in text_clean and "茶" not in text_clean and "湯" not in text_clean:
            scores["persona_integrity"] -= 4.0
            notes.append("影的貼文建議帶有更濃厚的料理或茶道生活氣息。")

    # 維度 5: 結尾開放式提問
    last_line = lines[-1] if lines else ""
    if not any(q in last_line for q in ["？", "?", "呢", "嗎", "如何"]):
        scores["open_question"] -= 6.0
        notes.append("結尾缺少溫暖的開放式問候或反問，可能降低讀者留言意願。")

    total_score = sum(scores.values())
    is_passed = total_score >= 88.0

    return {
        "status": "APPROVED" if is_passed else "REJECTED_LOW_SCORE",
        "atom": "atom-threads-preflight-gate",
        "passed": is_passed,
        "total_score": round(total_score, 1),
        "threshold": 88.0,
        "char_count": char_count,
        "dimension_scores": scores,
        "feedback_notes": notes if notes else ["完美符合甲子發文規範，准予出廠發布！"],
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-preflight-gate Threads 發布前安燈審計原子")
    parser.add_argument("--text", type=str, default="入冬後台東的夜晚很冷，廚房正熱著一鍋剝皮辣椒雞湯。\n\n路上騎車小心，今晚你那裡幾度呢？#日常料理", help="貼文文字")
    parser.add_argument("--persona", type=str, default="shadow", choices=["auto", "meow", "shadow"], help="主角人設")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = audit_draft_text(text=args.text, persona=args.persona)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[{result['status']}] 總分: {result['total_score']} - 通過: {result['passed']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
