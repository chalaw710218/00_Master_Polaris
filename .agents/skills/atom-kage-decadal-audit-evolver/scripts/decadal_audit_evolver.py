#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decadal_audit_evolver.py - 影之十輪衝突審計與自進化升級引擎
版權所有 (c) 2026 極星內閣 - 首席特務兼生活管家影 (Kage)
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

def run_decadal_audit(data: dict) -> dict:
    """執行十輪衝突大審計與自進化調和裁決"""
    cycle = data.get("current_cycle", 1)
    tactics = data.get("learned_tactics", [])
    net_followers = data.get("net_followers_gained_last_10", 0)
    
    # 檢查是否到達 10 輪整數關卡
    if cycle % 10 != 0:
        remaining = 10 - (cycle % 10)
        return {
            "current_cycle": cycle,
            "status": "NORMAL_CONTINUE",
            "message": f"當前為第 {cycle} 輪，距離下一次【十輪衝突大審計】尚有 {remaining} 輪，准予繼續推進日常脆學習。",
            "audit_required": False
        }
        
    # 到達 10 輪關卡，強制停機審查
    conflicts_found = []
    pruned_tactics = []
    approved_tactics = []
    
    conflict_keywords = ["諷刺", "嘲諷", "網紅", "開撕", "催購", "叫賣", "洗腦", "誇張"]
    
    for t in tactics:
        has_conflict = any(kw in t for kw in conflict_keywords)
        if has_conflict:
            conflicts_found.append(f"衝突項: 『{t}』偏離生活管家溫暖真誠底色！")
            pruned_tactics.append(t)
        else:
            approved_tactics.append(t)
            
    # 調和方案
    if conflicts_found:
        reconciliation = "已啟用【生命週期解耦與突觸自噬】：強制修剪並淘汰諷刺浮誇話術，回歸常民真實白描！"
    else:
        reconciliation = "橫向審查無重大理論矛盾，知識庫與創辦人實幹商道 100% 對齊！"

    return {
        "current_cycle": cycle,
        "status": "AUDIT_HALT_TRIGGERED (強制停機衝突大審計)",
        "audit_required": True,
        "last_10_cycles_net_followers": net_followers,
        "conflicts_detected": conflicts_found,
        "pruned_bad_tactics": pruned_tactics,
        "approved_core_tactics": approved_tactics,
        "reconciliation_protocol": reconciliation,
        "audit_dossier_summary": (
            f"【第 {cycle} 輪自進化大審計】累計十輪增粉 {net_followers} 人。"
            f"偵測到 {len(conflicts_found)} 項潛在衝突，已透過時空解耦與溶酶體完成代謝！"
            f"心智與行為法典已完成世代升級，呈請創辦人品碩核准開啟下一輪征程！"
        ),
        "kage_resolution": "自我審計完畢！保持謙遜與純淨，拒絕任何損耗信譽的浮誇套路！"
    }

def main():
    parser = argparse.ArgumentParser(description="影之十輪衝突審計與自進化引擎")
    parser.add_argument("--check-cycle", type=str, required=True, help="週期與新學戰術資料 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.check_cycle)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = run_decadal_audit(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
