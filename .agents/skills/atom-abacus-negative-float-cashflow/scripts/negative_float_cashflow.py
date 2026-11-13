#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
negative_float_cashflow.py - 負營運資金與產地現結套利精算引擎
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

def calculate_float_and_discount(data: dict) -> dict:
    """計算負營運資金指標與現金折讓年化套利"""
    rev = data.get("batch_revenue", 0)
    cost_nominal = data.get("farm_cost_nominal", 0)
    discount_rate = data.get("cash_discount_rate", 0.05)
    dsi = data.get("dsi_days", 2.0)
    dso = data.get("dso_days", 0.0)
    dpo = data.get("dpo_days", 5.0)
    advance_days = data.get("advance_days", 20)
    
    # 1. 現金轉換週期 CCC
    ccc = dsi + dso - dpo
    
    # 2. 現金折讓實質節省
    actual_cost = cost_nominal * (1 - discount_rate)
    cash_saved = cost_nominal * discount_rate
    effective_gross_profit = rev - actual_cost
    effective_margin = (effective_gross_profit / rev) if rev > 0 else 0.0
    
    # 3. 折讓年化投資回報率 (Annualized ROI)
    if (1 - discount_rate) > 0 and advance_days > 0:
        annualized_roi = (discount_rate / (1 - discount_rate)) * (365.0 / advance_days)
    else:
        annualized_roi = 0.0
        
    is_negative_float = ccc < 0
    status = "EXCELLENT_NEGATIVE_FLOAT" if is_negative_float else "WARNING_POSITIVE_FLOAT"
    
    return {
        "batch_financials": {
            "batch_revenue": rev,
            "cost_nominal": cost_nominal,
            "actual_cost_after_discount": round(actual_cost, 2),
            "instant_cash_arbitrage_saved": round(cash_saved, 2),
            "effective_gross_margin": f"{effective_margin:.1%}"
        },
        "working_capital_metrics": {
            "dsi_inventory_days": dsi,
            "dso_receivable_days": dso,
            "dpo_payable_days": dpo,
            "cash_conversion_cycle_days": round(ccc, 1),
            "float_status": status
        },
        "arbitrage_annualized_roi": f"{annualized_roi * 100:.1f}%",
        "munger_summary": (
            f"成功實現負營運資金 (CCC = {ccc:.1f} 天)！"
            f"以顧客預付款打小農現結，無風險憑空套出 NT$ {cash_saved:,.0f} 純利，"
            f"折讓年化回報率達 {annualized_roi * 100:.1f}%！"
            if is_negative_float else
            f"警示：現金轉換週期為正 ({ccc:.1f} 天)，存在營運資金壓迫，請強化預售集單！"
        )
    }

def main():
    parser = argparse.ArgumentParser(description="負營運資金與產地現結套利引擎")
    parser.add_argument("--calculate", type=str, required=True, help="訂單批次參數 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.calculate)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = calculate_float_and_discount(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
