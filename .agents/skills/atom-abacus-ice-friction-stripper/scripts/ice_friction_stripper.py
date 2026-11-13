#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ice_friction_stripper.py - 包冰淨重逆推與物流摩擦剝離精算引擎
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

def calculate_ice_glazing_true_cost(data: dict) -> dict:
    """計算包冰實質純肉成本逆推"""
    nominal = data.get("nominal_price", 0.0)
    ice_rate = data.get("ice_glazing_rate", 0.0)
    
    if ice_rate >= 1.0 or ice_rate < 0.0:
        return {"error": "包冰率需介於 0.0 與 0.99 之間"}
        
    net_meat_ratio = 1.0 - ice_rate
    true_meat_cost = nominal / net_meat_ratio if net_meat_ratio > 0 else nominal
    hidden_markup_pct = ((true_meat_cost - nominal) / nominal) if nominal > 0 else 0.0
    
    return {
        "nominal_quoted_price": nominal,
        "ice_glazing_rate": f"{ice_rate * 100:.1f}%",
        "net_meat_ratio": f"{net_meat_ratio * 100:.1f}%",
        "true_pure_meat_cost": round(true_meat_cost, 2),
        "hidden_water_markup": f"+{hidden_markup_pct * 100:.1f}%",
        "munger_negotiation_advice": (
            f"名義報價 NT$ {nominal} 看似便宜，實質純肉成本高達 NT$ {true_meat_cost:.2f}！"
            f"隱藏了 {hidden_markup_pct * 100:.1f}% 的自來水溢價！"
            f"採購合約全面強制要求以『0.0% 包冰實重報價』，否則一票否決！"
        )
    }

def calculate_logistics_friction_stripping(data: dict) -> dict:
    """計算末端物流摩擦剝離效益"""
    orders = data.get("total_orders", 0)
    courier_fee = data.get("traditional_courier_fee", 180.0)
    piggyback_fee = data.get("local_piggyback_fee", 50.0)
    
    saved_per_order = courier_fee - piggyback_fee
    total_friction_saved = saved_per_order * orders
    savings_pct = (saved_per_order / courier_fee) if courier_fee > 0 else 0.0
    
    return {
        "batch_volume": orders,
        "traditional_courier_unit_cost": courier_fee,
        "local_piggyback_unit_cost": piggyback_fee,
        "friction_saved_per_order": saved_per_order,
        "friction_savings_percentage": f"{savings_pct * 100:.1f}%",
        "total_friction_capital_recovered": total_friction_saved,
        "munger_insight": (
            f"成功從物流巨頭口中奪回 NT$ {total_friction_saved:,.0f} 元摩擦利潤！"
            f"每單省下 NT$ {saved_per_order:.0f} 元，轉化為車手生計與私域顧客好茶款待！"
        )
    }

def main():
    parser = argparse.ArgumentParser(description="包冰淨重逆推與物流摩擦剝離精算引擎")
    parser.add_argument("--ice-calc", type=str, help="包冰參數 (JSON 字串)")
    parser.add_argument("--logistics-calc", type=str, help="物流參數 (JSON 字串)")
    
    args = parser.parse_args()
    
    if args.ice_calc:
        try:
            i_data = json.loads(args.ice_calc)
            res = calculate_ice_glazing_true_cost(i_data)
        except Exception as e:
            print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
    elif args.logistics_calc:
        try:
            l_data = json.loads(args.logistics_calc)
            res = calculate_logistics_friction_stripping(l_data)
        except Exception as e:
            print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)
    else:
        print(json.dumps({"error": "請指定 --ice-calc 或 --logistics-calc"}, ensure_ascii=False))
        sys.exit(1)
        
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
