#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/layer_deconstructor.py
供應鏈四層摩擦與毛利精算底座
專精於 L3中盤 -> L2大盤 -> 物理耗損 -> 跨國海運關稅 -> L1產地FOB 嚴謹數學倒推
"""

import sys
import argparse
from typing import Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

# 品類專屬參數庫 (平均海運運費、關稅、物理耗損率、中盤常態加價率)
CATEGORY_COEFFICIENTS = {
    "seafood": {
        "name": "冷凍水產 (如智利鮭魚、草蝦)",
        "freight_tariff_ratio": 0.12,  # 跨國冷鏈海運 + 關稅檢疫約 12%
        "physical_loss_ratio": 0.08,   # 包冰、失水與化驗耗損約 8%
        "l2_margin_ratio": 0.15,       # 大盤合理利潤 15%
        "l3_margin_ratio": 0.20        # 中盤常態加價 20%
    },
    "meat": {
        "name": "進口原肉 (如澳洲牛肋條、美牛)",
        "freight_tariff_ratio": 0.14,  # 跨國空運/海運 + 關稅約 14%
        "physical_loss_ratio": 0.15,   # 修清油角、筋膜與化凍失水約 15%
        "l2_margin_ratio": 0.14,
        "l3_margin_ratio": 0.22
    },
    "nuts_dry": {
        "name": "堅果與進口乾貨 (如越南腰果、核桃)",
        "freight_tariff_ratio": 0.09,  # 常溫海運貨櫃 + 關稅約 9%
        "physical_loss_ratio": 0.05,   # 篩果與破裂損耗約 5%
        "l2_margin_ratio": 0.16,
        "l3_margin_ratio": 0.20
    },
    "local_vege": {
        "name": "在地生鮮蔬菜 (如台東高麗菜)",
        "freight_tariff_ratio": 0.05,  # 島內產地幹線物流約 5%
        "physical_loss_ratio": 0.12,   # 採收外葉剝除與運送耗損 12%
        "l2_margin_ratio": 0.12,
        "l3_margin_ratio": 0.18
    }
}

def deconstruct_supply_chain(item_name: str, quote_price: float, category: str = "seafood") -> Dict[str, Any]:
    """執行供應鏈四層摩擦與毛利精算"""
    coef = CATEGORY_COEFFICIENTS.get(category, CATEGORY_COEFFICIENTS["seafood"])

    # 1. 剝離 L3 中盤商加成 (取得 L2 進口大盤批發價)
    l3_markup_amount = round(quote_price * coef["l3_margin_ratio"], 1)
    l2_wholesale_price = round(quote_price - l3_markup_amount, 1)

    # 2. 剝離 L2 大盤商進口利潤
    l2_margin_amount = round(l2_wholesale_price * coef["l2_margin_ratio"], 1)
    landed_cost = round(l2_wholesale_price - l2_margin_amount, 1) # 到港落地成本 (CIF)

    # 3. 剝離物理耗損與修清成本
    loss_amount = round(landed_cost * coef["physical_loss_ratio"], 1)
    net_imported_goods_cost = round(landed_cost - loss_amount, 1)

    # 4. 剝離國際海空運、關稅與報驗摩擦 (還原 L1 產地出貨底價 FOB)
    friction_amount = round(net_imported_goods_cost * coef["freight_tariff_ratio"], 1)
    l1_fob_origin_price = round(net_imported_goods_cost - friction_amount, 1)

    # 5. 理論健康採購底價 (以到港成本 + 供應商 15% 總毛利為極限)
    theoretical_floor_price = round(landed_cost * 1.15, 1)
    excess_markup = round(max(0.0, quote_price - theoretical_floor_price), 1)
    markup_inflation_rate = round((excess_markup / quote_price) * 100, 1) if quote_price > 0 else 0.0

    return {
        "item_name": item_name,
        "category": coef["name"],
        "vendor_quote_l3": quote_price,
        "layers": {
            "l3_quoted_price": quote_price,
            "l3_middleman_markup": l3_markup_amount,
            "l2_wholesale_price": l2_wholesale_price,
            "l2_importer_margin": l2_margin_amount,
            "cif_landed_cost": landed_cost,
            "physical_loss_cost": loss_amount,
            "intl_freight_tariff": friction_amount,
            "l1_fob_origin_price": l1_fob_origin_price
        },
        "audit_metrics": {
            "theoretical_floor_price": theoretical_floor_price,
            "excess_markup_amount": excess_markup,
            "markup_inflation_rate": f"{markup_inflation_rate}%",
            "negotiable_target_range": f"NT$ {theoretical_floor_price} ~ {round((quote_price + theoretical_floor_price) / 2, 1)}"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="供應鏈四層摩擦與毛利精算底座")
    parser.add_argument("--item", type=str, default="智利冷凍鮭魚 (整尾原箱)", help="商品名稱")
    parser.add_argument("--quote", type=float, default=450.0, help="廠商報價 (元/公斤)")
    parser.add_argument("--category", type=str, default="seafood", choices=["seafood", "meat", "nuts_dry", "local_vege"], help="產業品類")
    parser.add_argument("--dry-run", action="store_true", help="執行四層精算模擬")
    args = parser.parse_args()

    res = deconstruct_supply_chain(args.item, args.quote, args.category)

    print("==================================================")
    print(f"⚓ 供應鏈四層毛利精算報告 (Exit Code: 0) - {res['item_name']}")
    print(f"品類分類: {res['category']} | 當前廠商報價 (L3): NT$ {res['vendor_quote_l3']} 元")
    print("--------------------------------------------------")
    print("層層倒推階層骨架:")
    print(f"  [L3 中盤報價]    : NT$ {res['layers']['l3_quoted_price']} 元 (包含中盤常態加成 NT$ {res['layers']['l3_middleman_markup']} 元)")
    print(f"  [L2 大盤批發價]  : NT$ {res['layers']['l2_wholesale_price']} 元 (包含大盤利潤 NT$ {res['layers']['l2_importer_margin']} 元)")
    print(f"  [CIF 到港落地價] : NT$ {res['layers']['cif_landed_cost']} 元")
    print(f"  [物理耗損與包冰] : NT$ {res['layers']['physical_loss_cost']} 元")
    print(f"  [國際運費與關稅] : NT$ {res['layers']['intl_freight_tariff']} 元")
    print(f"  👉 [L1 產地出貨價 FOB]: NT$ {res['layers']['l1_fob_origin_price']} 元")
    print("--------------------------------------------------")
    print(f"🎯 審計結論與底牌目標:")
    print(f"  - 理論健康採購底價: NT$ {res['audit_metrics']['theoretical_floor_price']} 元")
    print(f"  - 虛報隱形溢價空間: NT$ {res['audit_metrics']['excess_markup_amount']} 元 (溢價灌水率: {res['audit_metrics']['markup_inflation_rate']})")
    print(f"  - 建議殺價攻防區間: {res['audit_metrics']['negotiable_target_range']} 元")
    print("==================================================")

if __name__ == "__main__":
    main()
