#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontend_tech_evaluator.py - 尼奧前端前沿技術自主偵察與物理驗收引擎
版權所有 (c) 2026 極星內閣 - 首席前端架構師尼奧 (Neo)
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

def evaluate_frontend_technology(data: dict) -> dict:
    """執行前端前沿技術之常民實用性與物理指標自主審查"""
    tech_name = data.get("tech_name", "未知前端技術")
    gzip_kb = data.get("gzip_size_kb", 0.0)
    has_fallback = data.get("offline_fallback_ready", False)
    usefulness = data.get("rural_usefulness", "LOW").upper()
    solves_friction = data.get("solves_real_friction", False)
    
    veto_reasons = []
    score = 100
    
    # 1. 檢驗是否解決真實摩擦痛點 (反工程師自嗨炫技)
    if not solves_friction:
        veto_reasons.append("觸犯『反自嗨炫技律』：此技術未能解決常民用戶真實摩擦，屬於無效工程複雜度！")
        score -= 50
        
    # 2. 檢驗離線降級準備 (偏鄉孤島抗逆)
    if not has_fallback:
        veto_reasons.append("觸犯『偏鄉孤島離線優先律』：在弱網或不支援設備上缺乏優雅降級方案！")
        score -= 40
        
    # 3. 檢驗客戶端 Bundle 體積預算
    if gzip_kb > 50.0:
        veto_reasons.append(f"體積超標 (gzip: {gzip_kb}KB > 上限 50KB)！肥大 Runtime 將導致低階手機首屏白屏！")
        score -= 40
    elif gzip_kb > 30.0:
        score -= 15
        
    # 4. 偏鄉實用價值加權
    usefulness_bonus = 20 if usefulness == "HIGH" else (10 if usefulness == "MEDIUM" else 0)
    
    final_score = max(0, min(100, score - (len(veto_reasons) * 10) + usefulness_bonus))
    is_approved = len(veto_reasons) == 0 and final_score >= 80
    
    verdict = (
        "👑 尼奧技術驗收 100% 通過！准予納入極星核心前端武器庫，啟動原型開發！"
        if is_approved else
        f"❌ 一票否決！偵測到 {len(veto_reasons)} 項硬核缺失，判定為過度工程，禁止引入！"
    )

    return {
        "tech_name": tech_name,
        "is_approved": is_approved,
        "frontend_adoption_score": final_score,
        "metrics_evaluated": {
            "gzip_size_kb": gzip_kb,
            "offline_fallback_ready": has_fallback,
            "rural_usefulness_rating": usefulness,
            "solves_real_friction": solves_friction
        },
        "veto_reasons": veto_reasons,
        "neo_verdict": verdict
    }

def main():
    parser = argparse.ArgumentParser(description="尼奧前端技術自主篩選引擎")
    parser.add_argument("--evaluate-tech", type=str, required=True, help="受檢前端技術資料 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.evaluate_tech)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = evaluate_frontend_technology(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
