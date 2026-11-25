#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sopk_attribution_engine.py - 戴明深層知識體系與94/6系統歸因審計引擎
版權所有 (c) 2026 極星內閣 - 首席品質長戴明 (Dr. Deming)
"""

import sys
import json
import argparse
import math

def calculate_spc(values: list, usl: float, lsl: float) -> dict:
    """計算統計變異指標、Cpk 與韋斯頓電氣四規則"""
    n = len(values)
    if n < 3:
        return {"error": "數據點過少，至少需 3 個樣本"}
        
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    std_dev = math.sqrt(variance) if variance > 0 else 0.0001
    
    # 計算 Cpk
    cpu = (usl - mean) / (3 * std_dev)
    cpl = (mean - lsl) / (3 * std_dev)
    cpk = min(cpu, cpl)
    
    # 韋斯頓電氣四規則審計
    rules_triggered = []
    
    # Rule 1: 單點超出 3 sigma
    for i, x in enumerate(values):
        if abs(x - mean) > 3 * std_dev:
            rules_triggered.append(f"規則1 (特殊變異): 第 {i+1} 點 ({x}) 超出 3-Sigma 警戒線")
            
    # Rule 2: 連續 3 點中有 2 點落在 2 sigma 之外 (同一側)
    for i in range(len(values) - 2):
        window = values[i:i+3]
        upper_2sigma = sum(1 for x in window if x > mean + 2 * std_dev)
        lower_2sigma = sum(1 for x in window if x < mean - 2 * std_dev)
        if upper_2sigma >= 2 or lower_2sigma >= 2:
            rules_triggered.append(f"規則2 (趨勢警訊): 視窗 [{i+1}~{i+3}] 有 2 點超出 2-Sigma (同側)")
            break
            
    # Rule 4: 連續 8 點在中心線同一側
    side_streak = 0
    current_side = 0
    for x in values:
        side = 1 if x > mean else (-1 if x < mean else 0)
        if side != 0 and side == current_side:
            side_streak += 1
            if side_streak >= 8:
                rules_triggered.append("規則4 (系統漂移): 連續 8 點落在平均線同一側")
                break
        else:
            current_side = side
            side_streak = 1

    # 判定變異類別與瞎折騰 (Tampering) 警示
    if not rules_triggered:
        variation_type = "COMMON_CAUSE (常態固有變異)"
        action_advice = "嚴禁盲目手動微調 (Non-Tampering)！系統處於統計受控狀態，胡亂干預將放大四倍變異。"
    else:
        variation_type = "SPECIAL_CAUSE (特殊外部變異)"
        action_advice = "檢測到特殊變異！啟動隔離診斷與外生干擾排查，不可直接責怪常規作業。"

    return {
        "sample_size": n,
        "mean": round(mean, 4),
        "std_dev": round(std_dev, 4),
        "cpk": round(cpk, 2),
        "cpk_evaluation": "優秀 (>=1.33)" if cpk >= 1.33 else ("可接受 (1.0~1.33)" if cpk >= 1.0 else "不足 (<1.0 需治理)"),
        "rules_triggered": rules_triggered,
        "variation_type": variation_type,
        "action_advice": action_advice
    }

def audit_incident_attribution(report: dict) -> dict:
    """審計事故報告之 94/6 責任歸因"""
    incident = report.get("incident", "未知事故")
    claimed_blame = report.get("claimed_blame", "")
    system_context = report.get("system_context", {})
    
    # 識別報告是否把責任甩給基層個人
    worker_blame_keywords = ["粗心", "不細心", "責任心不足", "偷懶", "疏忽", "個人失誤", "沒注意"]
    is_blaming_worker = any(kw in claimed_blame for kw in worker_blame_keywords)
    
    # 檢驗系統本身防呆與流程支援度
    system_flaws_found = []
    for k, v in system_context.items():
        if v is True:
            system_flaws_found.append(k)
            
    # 戴明 94/6 裁決
    if is_blaming_worker:
        deming_verdict = "REJECTED (駁回甩鍋報告)"
        corrected_attribution = "94% 系統責任 (Systemic Attribution)"
        commentary = (
            f"原報告將『{incident}』歸咎於『{claimed_blame}』，嚴重違反戴明第4律 (94/6 責任律)！"
            f"若流程設計允許人員因疲倦或分心而出錯，責任 100% 在於管理層未設置 Poka-Yoke 防呆機關。"
        )
    else:
        deming_verdict = "ACCEPTED (符合戴明原則)"
        corrected_attribution = "系統流程與環境持續改善"
        commentary = "報告客觀聚焦於流程漏洞與器具改善，維護一線夥伴心理安全。"

    recommended_pokayoke = [
        f"在流程中部署防呆阻斷: 針對 {flaw} 建立物理/數位不可做錯機制"
        for flaw in (system_flaws_found if system_flaws_found else ["操作界面明確性", "前置雙重檢驗"])
    ]

    return {
        "incident": incident,
        "claimed_blame": claimed_blame,
        "deming_verdict": deming_verdict,
        "corrected_attribution": corrected_attribution,
        "system_flaws_identified": system_flaws_found,
        "commentary": commentary,
        "recommended_pokayoke": recommended_pokayoke
    }

def main():
    parser = argparse.ArgumentParser(description="戴明 SoPK 與 94/6 歸因審計引擎")
    parser.add_argument("--mode", choices=["spc", "incident"], required=True, help="審計模式")
    parser.add_argument("--values", type=str, help="數值清單 (逗號分隔，用於 spc 模式)")
    parser.add_argument("--usl", type=float, default=100.0, help="規格上限 USL")
    parser.add_argument("--lsl", type=float, default=0.0, help="規格下限 LSL")
    parser.add_argument("--report", type=str, help="事故報告 (JSON 字串，用於 incident 模式)")
    
    args = parser.parse_args()
    
    if args.mode == "spc":
        if not args.values:
            print(json.dumps({"error": "缺少 --values 參數"}, ensure_ascii=False))
            sys.exit(1)
        try:
            val_list = [float(v.strip()) for v in args.values.split(",") if v.strip()]
            res = calculate_spc(val_list, args.usl, args.lsl)
        except Exception as e:
            print(json.dumps({"error": f"解析數值失敗: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
    else:
        if not args.report:
            print(json.dumps({"error": "缺少 --report 參數"}, ensure_ascii=False))
            sys.exit(1)
        try:
            rep_data = json.loads(args.report)
            res = audit_incident_attribution(rep_data)
        except Exception as e:
            print(json.dumps({"error": f"解析報告 JSON 失敗: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
            
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
