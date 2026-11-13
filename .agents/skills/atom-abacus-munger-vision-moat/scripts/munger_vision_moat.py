#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
munger_vision_moat.py - 查理·蒙格百年遠見與複利護城河評估引擎
版權所有 (c) 2026 極星內閣 - 財務長算盤 (Abacus / Charlie Munger)
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

def evaluate_munger_vision(proposal: dict) -> dict:
    """執行查理·蒙格多階因果效應與十年護城河評估"""
    name = proposal.get("name", "未命名提案")
    margin_1st = proposal.get("short_term_margin", 0.0)
    rep_impact = proposal.get("reputation_impact", "NEUTRAL").upper()
    reorder_pot = proposal.get("reorder_potential", "MEDIUM").upper()
    ecosystem_win = proposal.get("ecosystem_win_win", False)
    cigar_butt = proposal.get("has_cigar_butt_greed", False)
    
    veto_reasons = []
    
    # 1. 蒙格第一鐵律：雪茄屁股一票否決
    if cigar_butt:
        veto_reasons.append("觸犯『雪茄屁股律』：屬於短視近利的平庸廉價投機，消耗品牌珍貴信譽！")
        
    # 2. 商譽負面衝擊一票否決
    if rep_impact in ["NEGATIVE", "HIGH_NEGATIVE"]:
        veto_reasons.append(f"商譽衝擊為 {rep_impact}！蒙格戒律：信譽需要二十年建立，五分鐘毀掉！")
        
    # 3. 多階效應與羅拉帕魯札指數推演
    # 第一階分數 (短期毛利)
    s1_score = min(30, int(margin_1st * 100))
    
    # 第二階分數 (顧客回購與LTV信賴)
    s2_map = {"HIGH": 35, "MEDIUM": 20, "LOW": 5}
    s2_score = s2_map.get(reorder_pot, 15)
    
    # 第三階分數 (生態共生與多重正向共振)
    s3_score = 35 if ecosystem_win else 10
    
    foresight_score = s1_score + s2_score + s3_score
    
    # 護城河評級
    if veto_reasons:
        moat_rating = "VETOED_CIGAR_BUTT"
        verdict = "❌ 蒙格一票否決！缺乏遠見之短視提案，禁止放行！"
        passed = False
    elif foresight_score >= 85:
        moat_rating = "AAA_WIDE_MOAT_FORTRESS (特寬護城河堡壘)"
        verdict = "👑 蒙格遠見至高評定！具備十年信譽複利與羅拉帕魯札共振效應，全力推進！"
        passed = True
    elif foresight_score >= 65:
        moat_rating = "AA_NARROW_MOAT (常態優良護城河)"
        verdict = "✅ 合格！具備良好第二階效應，商業健康度良好。"
        passed = True
    else:
        moat_rating = "B_MARGINAL_VALUE (護城河薄弱)"
        verdict = "⚠️ 警示：長期抗風險與顧客黏著力不足，需重構商業模式。"
        passed = False

    return {
        "proposal_name": name,
        "is_passed": passed,
        "moat_rating": moat_rating,
        "munger_foresight_score": foresight_score,
        "multi_order_analysis": {
            "first_order_margin": f"{margin_1st:.1%}",
            "second_order_reorder": reorder_pot,
            "third_order_ecosystem": "WIN_WIN" if ecosystem_win else "ISOLATED",
        },
        "veto_reasons": veto_reasons,
        "munger_verdict": verdict
    }

def main():
    parser = argparse.ArgumentParser(description="查理·蒙格百年遠見與複利護城河引擎")
    parser.add_argument("--proposal", type=str, required=True, help="受檢商業提案 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.proposal)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = evaluate_munger_vision(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
