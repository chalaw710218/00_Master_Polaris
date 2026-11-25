#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
survival_reservoir_opex.py - 114天極限無債生存水庫與三角分潤精算引擎
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

def audit_survival_reservoir(data: dict) -> dict:
    """審計極限無債生存水庫水位與存活天數"""
    monthly_burn = data.get("monthly_opex_burn", 30000.0)
    current_cash = data.get("current_cash_reserve", 0.0)
    
    # 蒙格 114 天標準 (3.8 個月)
    target_months = 3.8
    target_days = int(target_months * 30)
    target_reserve = monthly_burn * target_months
    
    if monthly_burn > 0:
        actual_survival_days = (current_cash / monthly_burn) * 30.0
        coverage_months = current_cash / monthly_burn
    else:
        actual_survival_days = 999.0
        coverage_months = 99.0
        
    is_fortress_passed = actual_survival_days >= target_days
    
    return {
        "monthly_opex_burn": monthly_burn,
        "current_cash_reserve": current_cash,
        "target_safety_reserve_3_8_months": target_reserve,
        "actual_survival_days": round(actual_survival_days, 1),
        "actual_coverage_months": round(coverage_months, 2),
        "target_baseline_days": target_days,
        "fortress_status": "FORTRESS_SECURE (堡壘安全)" if is_fortress_passed else "RESERVOIR_DEFICIT (水庫吃緊)",
        "commentary": (
            f"堡壘防線固若金湯！在零營收極端黑天鵝衝擊下，公司可無債安然存活 {actual_survival_days:.0f} 天，"
            f"完全超越 114 天軍規！"
            if is_fortress_passed else
            f"警告：當前水位僅可存活 {actual_survival_days:.0f} 天，低於 114 天標準，"
            f"尚需注水 NT$ {(target_reserve - current_cash):,.0f} 元！"
        )
    }

def calculate_delivery_sharing(data: dict) -> dict:
    """計算市區外送與友店自取之三角分潤及金庫注水"""
    d_orders = data.get("delivery_orders", 0)
    p_orders = data.get("pickup_orders", 0)
    
    # 外送單 (收 50 元)
    rider_total = d_orders * 40.0
    d_reserve_total = d_orders * 5.0
    d_company_total = d_orders * 5.0
    
    # 自提單 (補貼 25 元)
    depot_total = p_orders * 15.0
    p_reserve_total = p_orders * 5.0
    p_company_total = p_orders * 5.0
    
    total_reserve_inflow = d_reserve_total + p_reserve_total
    total_company_retained = d_company_total + p_company_total
    
    return {
        "order_volume": {
            "delivery_orders": d_orders,
            "pickup_orders": p_orders,
            "total_orders": d_orders + p_orders
        },
        "payouts": {
            "rider_payout": rider_total,
            "depot_payout": depot_total,
            "total_community_partner_income": rider_total + depot_total
        },
        "treasury_inflow": {
            "opex_reservoir_inflow": total_reserve_inflow,
            "company_retained_net": total_company_retained
        },
        "munger_governance": "三角分潤自體循環建立！夥伴賺取生計，同時為 114 天水庫注水！"
    }

def main():
    parser = argparse.ArgumentParser(description="114天極限無債生存水庫與三角分潤精算引擎")
    parser.add_argument("--audit-reservoir", type=str, help="水庫審查參數 (JSON 字串)")
    parser.add_argument("--calc-delivery", type=str, help="物流訂單參數 (JSON 字串)")
    
    args = parser.parse_args()
    
    if args.audit_reservoir:
        try:
            r_data = json.loads(args.audit_reservoir)
            res = audit_survival_reservoir(r_data)
        except Exception as e:
            print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
    elif args.calc_delivery:
        try:
            d_data = json.loads(args.calc_delivery)
            res = calculate_delivery_sharing(d_data)
        except Exception as e:
            print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
    else:
        print(json.dumps({"error": "請指定 --audit-reservoir 或 --calc-delivery"}, ensure_ascii=False))
        sys.exit(1)
        
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
