#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
joy_flow_allocator.py - 戴明 80/20 彈性心流與工作自豪感調配引擎
版權所有 (c) 2026 極星內閣 - 首席品質長戴明 (Dr. Deming)
"""

import sys
import json
import argparse

# 強制 Windows 環境標準輸出採用 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def evaluate_task(task_data: dict) -> dict:
    """評估作業之 80% 鋼鐵安全底線與 20% 人性心流溢價"""
    safety_checks = task_data.get("safety_checks", {})
    warmth_actions = task_data.get("human_warmth_actions", [])
    
    # 1. 審查 80% 鋼鐵安全底線 (一票否決)
    breached_safeties = []
    for rule, passed in safety_checks.items():
        if not passed:
            breached_safeties.append(rule)
            
    if breached_safeties:
        return {
            "status": "REJECTED_SAFETY_BREACH",
            "is_passed": False,
            "ironclad_safety_score": 0,
            "breached_rules": breached_safeties,
            "verdict": "觸犯 80% 鋼鐵安全底線！任何人性關懷不能建立在虧損或洩漏資安之上，拉下安燈繩！"
        }
        
    # 2. 評估 20% 人性自主心流 (品質溢價)
    warmth_score = min(20, len(warmth_actions) * 10)
    total_quality_score = 80 + warmth_score
    
    if warmth_actions:
        verdict_status = "PASSED_WITH_JOY_HONOR"
        title = "👑 戴明至樂品質榮譽放行 (Highest Joy in Work Honor)"
        commentary = (
            f"前線夥伴在守死 80% 安全底線下，自發付出了 {len(warmth_actions)} 項人性關懷！"
            f"認定為極星最高品質溢價，享有全域免責與表彰保護。"
        )
    else:
        verdict_status = "STANDARD_COMPLIANT"
        title = "✅ 標準合規放行 (Standard Compliant)"
        commentary = "作業完全符合 80% 安全基準線，流程順暢。"

    return {
        "status": verdict_status,
        "is_passed": True,
        "title": title,
        "ironclad_safety_score": 80,
        "elastic_warmth_score": warmth_score,
        "total_deming_score": total_quality_score,
        "warmth_actions_recorded": warmth_actions,
        "commentary": commentary
    }

def evaluate_manager(manager_data: dict) -> dict:
    """評估管理者「基層工作障礙清除率」KPI"""
    reported = manager_data.get("impediments_reported", 0)
    cleared = manager_data.get("impediments_cleared", 0)
    
    if reported == 0:
        icr = 1.0
    else:
        icr = cleared / reported
        
    is_deming_standard = icr >= 0.90
    
    return {
        "impediments_reported": reported,
        "impediments_cleared": cleared,
        "clearance_rate": f"{icr * 100:.1f}%",
        "deming_leadership_evaluation": "DEMING_LEADERSHIP_EXCELLENCE (卓越障礙清除者)" if is_deming_standard else "BUREAUCRACY_ALERT (需強化基層障礙掃除)",
        "guidance": (
            "戴明教導：管理者的唯一目的，是幫助所有人與機器把工作做得更好！"
            if is_deming_standard else
            "警告：清除率低於 90%，請立即放下考勤與表格，親赴一線為夥伴拆除工具與流程摩擦障礙！"
        )
    }

def main():
    parser = argparse.ArgumentParser(description="戴明 80/20 彈性心流調配引擎")
    parser.add_argument("--eval-task", type=str, help="前線作業資料 (JSON 字串)")
    parser.add_argument("--eval-manager", type=str, help="管理者數據 (JSON 字串)")
    
    args = parser.parse_args()
    
    if args.eval_task:
        try:
            t_data = json.loads(args.eval_task)
            res = evaluate_task(t_data)
        except Exception as e:
            print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
    elif args.eval_manager:
        try:
            m_data = json.loads(args.eval_manager)
            res = evaluate_manager(m_data)
        except Exception as e:
            print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
    else:
        print(json.dumps({"error": "請指定 --eval-task 或 --eval-manager"}, ensure_ascii=False))
        sys.exit(1)
        
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
