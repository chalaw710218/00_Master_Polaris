#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/pack_qu_guang_guang.py
====================================================================
🚶‍♂️ pack-qu-guang-guang 【去逛逛 · 全自動社群漫遊技能組】
組裝 5 大萬用原子：
1. atom-trend-scout (熱點降維)
2. atom-meow-voice (真貓生態)
3. atom-kage-clout-tea (管家端茶)
4. atom-growth-quality-gate (戴明安燈)
5. atom-threads-engine (確定性傳輸)
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

# 確保 scripts 目錄在 sys.path 中
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

# 動態引用 scripts 目錄下的萬用原子
from trend_scout_deep import fetch_real_trends
from meow_voice_deep import generate_meow_voice
from kage_tea_deep import serve_tea
from quality_gate_deep import audit_quality
from threads_engine_deep import execute_threads_transmission

def run_qu_guang_guang_pipeline(dry_run: bool = False, role_choice: str = "auto") -> Dict[str, Any]:
    """執行『去逛逛』全自動管線"""
    pipeline_report = {
        "pipeline": "pack-qu-guang-guang",
        "status": "in_progress",
        "stages": {}
    }

    # Stage 1: 嗅探熱點 (atom-trend-scout)
    trends = fetch_real_trends(limit=1)
    primary_topic = trends[0]
    pipeline_report["stages"]["trend_scout"] = {
        "title": primary_topic["raw_keyword"],
        "angle": primary_topic["three_conversions_angle"],
        "folk_emotion": primary_topic["folk_emotion"],
        "plot": primary_topic["narrative_hook_plot"],
        "source": primary_topic["source"]
    }

    # Stage 2: 雙主角視角生成 (atom-meow-voice 或 atom-kage-clout-tea)
    context_text = f"今日時事【{primary_topic['raw_keyword']}】：{primary_topic['narrative_hook_plot']}"
    
    if role_choice == "auto":
        # 若情境偏打工辛勞/天氣則由管家端茶，否則由店貓破防
        chosen_role = "kage" if any(k in primary_topic["raw_keyword"] for k in ["天", "雨", "冷", "累", "病", "防護"]) else "meow"
    else:
        chosen_role = role_choice

    if chosen_role == "meow":
        voice_result = generate_meow_voice(input_text=context_text)
        speech_text = f"{voice_result['full_reply']}\n\n#生活的一部分就醬點 #店貓隨筆"
        pipeline_report["stages"]["voice_generator"] = {
            "role": "喵編 (Meow Editor)",
            "state": voice_result["state"],
            "speech": voice_result["full_reply"]
        }
    else:
        tea_result = serve_tea(input_text=context_text)
        speech_text = f"{tea_result['tea_speech']}\n\n#生活的一部分就醬點 #生活管家"
        pipeline_report["stages"]["voice_generator"] = {
            "role": "影 (Kage · 生活管家)",
            "mode": tea_result["mode"],
            "speech": tea_result["tea_speech"]
        }

    # Stage 3: 戴明安燈品質閘門 (atom-growth-quality-gate)
    audit_result = audit_quality(speech_text)
    pipeline_report["stages"]["quality_gate"] = audit_result

    if audit_result["status"] != "PASS":
        pipeline_report["status"] = "HALTED_BY_ANDON"
        pipeline_report["error"] = audit_result.get("fatal_violation") or audit_result.get("feedback")
        return pipeline_report

    # Stage 4: 確定性傳輸 (atom-threads-engine)
    transmission_result = execute_threads_transmission(
        text=speech_text,
        dry_run=dry_run
    )
    pipeline_report["stages"]["transmission"] = transmission_result
    pipeline_report["status"] = "SUCCESS"
    pipeline_report["final_post_id"] = transmission_result.get("threads_post_id")
    pipeline_report["final_text"] = speech_text

    return pipeline_report

def main():
    parser = argparse.ArgumentParser(description="pack-qu-guang-guang 【去逛逛 · 全自動社群漫遊技能組】")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬漫遊")
    parser.add_argument("--role", type=str, default="auto", choices=["auto", "meow", "kage"], help="指定漫遊主角")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    report = run_qu_guang_guang_pipeline(dry_run=args.dry_run, role_choice=args.role)
    
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"[{report['status']}] 發布成果: {report.get('final_post_id')}")
        print(f"發布內文:\n{report.get('final_text')}")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
