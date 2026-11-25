#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/pricing_5d_calculator.py
創辦人原創 5D 商業價值矩陣多型精算底座
支援 5D-Labor / 5D-Impact / 5D-Asset 三大模態純淨數學運算與蒙格現金流風控
"""

import sys
import math
import argparse
from typing import Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

# 基礎費率與安全邊際常數
BASE_HOURLY_RATE_LABOR = 250   # 勞務基礎時薪基準 (新台幣)
MIN_LABOR_PRICE = 200          # 勞務最低起步保護價 (新台幣)
MIN_IMPACT_PRICE = 6000        # 顧問成果最低留任金 (新台幣)
MIN_ASSET_PRICE = 399          # 數位資產/課程最低保護價 (新台幣)

def assess_advance_payment_risk(amount: float) -> Dict[str, Any]:
    """查理·蒙格代墊款三色燈風控評估"""
    if amount <= 1000:
        return {
            "level": "GREEN",
            "tag": "🟢 綠燈 (常規代墊)",
            "policy": "由管家現場代墊，憑實體發票或免用統一發票收據於交付時現場結清。"
        }
    elif amount <= 2000:
        return {
            "level": "YELLOW",
            "tag": "🟡 黃燈 (信用確認)",
            "policy": "需委託人提供即時網銀轉帳證明截圖或官方 LINE OA 信用擔保確認。"
        }
    else:
        return {
            "level": "RED",
            "tag": "🔴 紅燈 (強制預付防線)",
            "policy": "強制啟動預付防線！貨款超過 NT$ 2,000 元，委託人必須於出勤前全額匯入指定帳戶，管家方可出勤代購，杜絕壞帳與無息墊資。"
        }

def calculate_5d_labor(
    minutes: int,
    d1: float = 1.0,
    d2: float = 1.0,
    d3: float = 1.0,
    d4: float = 1.0,
    d5: float = 1.0,
    item_value: float = 0.0,
    hourly_rate: float = BASE_HOURLY_RATE_LABOR
) -> Dict[str, Any]:
    """5D-Labor 勞務工時型精算"""
    base_hours = max(0.5, minutes / 60.0)
    multiplier = d1 * d2 * d3 * d4 * d5
    tp_hours = base_hours * multiplier
    raw_price = tp_hours * hourly_rate
    # 向上百位數或五十位數取整，保護利潤
    final_price = max(MIN_LABOR_PRICE, int(math.ceil(raw_price / 10.0) * 10))

    risk = assess_advance_payment_risk(item_value)

    return {
        "mode": "5D-Labor (勞務工時防禦型)",
        "base_minutes": minutes,
        "base_hours": round(base_hours, 2),
        "factors": {"D1_friction": d1, "D2_risk": d2, "D3_expertise": d3, "D4_urgency": d4, "D5_trust": d5},
        "total_multiplier": round(multiplier, 3),
        "tp_effective_hours": round(tp_hours, 2),
        "hourly_rate": hourly_rate,
        "raw_computed_price": round(raw_price, 1),
        "final_service_price": final_price,
        "item_advance_value": item_value,
        "total_collectible": final_price + item_value,
        "advance_payment_risk": risk
    }

def calculate_5d_impact(
    value_impact: float,
    d2: float = 1.5,
    d3: float = 2.0,
    d4: float = 1.5,
    d5: float = 1.2,
    base_cut_ratio: float = 0.08
) -> Dict[str, Any]:
    """5D-Impact 成果價值捕獲型精算"""
    # 價值捕獲加乘係數
    multiplier = (d3 * d4 * d2 * d5) / 3.0
    captured_value = value_impact * base_cut_ratio * multiplier
    final_price = max(MIN_IMPACT_PRICE, int(math.ceil(captured_value / 500.0) * 500))

    return {
        "mode": "5D-Impact (成果價值捕獲型)",
        "value_impact": value_impact,
        "base_cut_ratio": base_cut_ratio,
        "factors": {"D2_risk": d2, "D3_expertise": d3, "D4_urgency": d4, "D5_trust": d5},
        "impact_multiplier": round(multiplier, 3),
        "captured_value": round(captured_value, 1),
        "final_service_price": final_price
    }

def calculate_5d_asset(
    fixed_dev_cost: float,
    marginal_cost: float,
    target_volume: int,
    d1: float = 1.0,
    d2: float = 1.0,
    d3: float = 1.5,
    d4: float = 1.0,
    d5: float = 1.2
) -> Dict[str, Any]:
    """5D-Asset 數位資產規模型精算"""
    unit_base = (fixed_dev_cost / max(1, target_volume)) + marginal_cost
    multiplier = d1 * d2 * d3 * d4 * d5
    raw_unit_price = unit_base * multiplier
    final_unit_price = max(MIN_ASSET_PRICE, int(math.ceil(raw_unit_price / 10.0) * 10))

    return {
        "mode": "5D-Asset (數位資產規模型)",
        "fixed_dev_cost": fixed_dev_cost,
        "marginal_cost": marginal_cost,
        "target_volume": target_volume,
        "unit_base_cost": round(unit_base, 1),
        "factors": {"D1_friction": d1, "D2_risk": d2, "D3_expertise": d3, "D4_urgency": d4, "D5_trust": d5},
        "asset_multiplier": round(multiplier, 3),
        "raw_unit_price": round(raw_unit_price, 1),
        "final_unit_price": final_unit_price
    }

def main():
    parser = argparse.ArgumentParser(description="創辦人原創 5D 商業價值矩陣多型精算底座")
    parser.add_argument("--mode", type=str, default="labor", choices=["labor", "impact", "asset"], help="定價模態")
    parser.add_argument("--minutes", type=int, default=45, help="勞務工時 (分鐘)")
    parser.add_argument("--value-impact", type=float, default=500000.0, help="挽救或創造之成果總價值")
    parser.add_argument("--fixed-cost", type=float, default=60000.0, help="資產固定研發成本")
    parser.add_argument("--marginal-cost", type=float, default=25.0, help="資產單份履約邊際成本")
    parser.add_argument("--volume", type=int, default=300, help="預期資產規模")
    parser.add_argument("--item-value", type=float, default=2400.0, help="託購商品代墊金額 (元)")
    parser.add_argument("--d1", type=float, default=1.2, help="D1 摩擦力係數")
    parser.add_argument("--d2", type=float, default=1.3, help="D2 風險承擔係數")
    parser.add_argument("--d3", type=float, default=1.2, help="D3 技術門檻係數")
    parser.add_argument("--d4", type=float, default=1.0, help="D4 時效槓桿係數")
    parser.add_argument("--d5", type=float, default=1.2, help="D5 情緒信任係數")
    parser.add_argument("--dry-run", action="store_true", help="執行精算模擬")
    args = parser.parse_args()

    if args.mode == "labor":
        res = calculate_5d_labor(
            minutes=args.minutes,
            d1=args.d1, d2=args.d2, d3=args.d3, d4=args.d4, d5=args.d5,
            item_value=args.item_value
        )
    elif args.mode == "impact":
        res = calculate_5d_impact(
            value_impact=args.value_impact,
            d2=args.d2, d3=args.d3, d4=args.d4, d5=args.d5
        )
    else:
        res = calculate_5d_asset(
            fixed_dev_cost=args.fixed_cost,
            marginal_cost=args.marginal_cost,
            target_volume=args.volume,
            d1=args.d1, d2=args.d2, d3=args.d3, d4=args.d4, d5=args.d5
        )

    print("==================================================")
    print(f"🧮 5D 商業價值矩陣精算完成 (Exit Code: 0) - {res['mode']}")
    print("--------------------------------------------------")
    print(f"五維係數設定: {res['factors']}")
    if args.mode == "labor":
        print(f"基礎投入工時: {res['base_minutes']} 分鐘 ({res['base_hours']} 小時)")
        print(f"5D 總連乘乘數: {res['total_multiplier']}x | 換算實質價值工時 (TP): {res['tp_effective_hours']} 小時")
        print(f"👉 建議管家服務費: NT$ {res['final_service_price']} 元 (時薪基準: {res['hourly_rate']} 元/時，保底: {MIN_LABOR_PRICE} 元)")
        if res['item_advance_value'] > 0:
            print(f"📦 代墊商品貨款: NT$ {res['item_advance_value']} 元")
            print(f"💰 總應收金額 (服務費+貨款): NT$ {res['total_collectible']} 元")
            print("--------------------------------------------------")
            print(f"🛡️ 查理·蒙格代墊款風控審查: {res['advance_payment_risk']['tag']}")
            print(f"  [風控指引] {res['advance_payment_risk']['policy']}")
    elif args.mode == "impact":
        print(f"挽救/創造之價值: NT$ {res['value_impact']:,} 元")
        print(f"成果捕獲乘數: {res['impact_multiplier']}x")
        print(f"👉 建議專案諮詢費: NT$ {res['final_service_price']:,} 元 (起步保底: NT$ {MIN_IMPACT_PRICE:,} 元)")
    else:
        print(f"固定研發成本: NT$ {res['fixed_dev_cost']:,} 元 | 邊際成本: NT$ {res['marginal_cost']} 元 | 目標規模: {res['target_volume']} 份")
        print(f"資產溢價乘數: {res['asset_multiplier']}x")
        print(f"👉 建議單份定價: NT$ {res['final_unit_price']} 元 (最低保護價: NT$ {MIN_ASSET_PRICE} 元)")
    print("==================================================")

if __name__ == "__main__":
    main()
