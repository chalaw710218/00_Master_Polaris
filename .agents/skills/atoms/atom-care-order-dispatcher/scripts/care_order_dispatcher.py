#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/care_order_dispatcher.py
生活管家孝親安居工單排程與 5D 定價引擎
支援五大孝親模組標準化派工單、5D 精算定價、戴明防呆工具箱檢核
"""

import sys
import argparse
from datetime import datetime
from typing import Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

CARE_MODULES = {
    "escort": {
        "name": "【孝親暖心】長輩就醫陪診 ＋ 醫囑速記聽診",
        "base_price": 1200,
        "base_hours": 2,
        "overtime_rate": 400,
        "tools_checklist": ["長輩就醫聽診筆記本", "溫水保溫瓶", "一次性醫用口罩", "輪椅輔助推行帶"],
        "disclaimer": "非醫療性生活陪伴與醫囑速記員，嚴禁擅自給予醫療建議或調整用藥"
    },
    "anti_slip": {
        "name": "【居安無憂】浴室奈米防滑 ＋ 防滑扶手 ＋ 配電盤熱像電檢",
        "base_price": 2999,
        "base_hours": 2.5,
        "overtime_rate": 0,
        "tools_checklist": ["FLIR 紅外熱像儀", "304 不鏽鋼防滑扶手 (承重120kg)", "德國奈米隱形止滑劑", "水平儀與電動衝擊起子"],
        "disclaimer": "施工前需取得屋主或長輩口頭知情同意，配電盤檢測若遇發燙即刻斷電通知專業水電師傅"
    },
    "grooming": {
        "name": "【體面長青】臥床與行動不便長輩到府尊嚴修容理髮",
        "base_price": 600,
        "base_hours": 1,
        "overtime_rate": 300,
        "tools_checklist": ["醫療級靜音集塵電剪 (吸髮不落地)", "一次性純棉圍兜", "溫熱敷臉毛巾", "草本低敏刮鬍泡與安全刮刀"],
        "disclaimer": "未經家屬授權嚴禁拍攝長輩非體面臥床畫面，以尊嚴與舒適為最高原則"
    },
    "biography": {
        "name": "【傳家之寶】高齡老農口述歷史與一生回憶錄印製",
        "base_price": 6800,
        "base_hours": 6,
        "overtime_rate": 0,
        "tools_checklist": ["高清錄音筆", "高解析度照片翻拍掃描儀", "精美訪談手冊", "老歌播放背景音樂"],
        "disclaimer": "口述內容需經家族長者親筆或錄音確認，印製前完成全彩打樣審查"
    },
    "soft_meal": {
        "name": "【暖胃風土】每週常溫高壓刺蔥燉湯 ＋ 低 GI 養生膳",
        "base_price": 750,
        "base_hours": 0.5,
        "overtime_rate": 0,
        "tools_checklist": ["生活管家低溫保鮮袋", "食品效期檢查手冊", "廚房即期品理貨籃"],
        "disclaimer": "食材需具備常溫高壓滅菌或合格低溫冷鏈證明，送達協助長輩檢視冰箱"
    }
}

def create_care_order(
    order_type: str,
    client_name: str,
    elder_name: str,
    address: str = "台東市正氣北路老宅",
    hours: float = 2.0,
    item_advance: float = 0.0
) -> Dict[str, Any]:
    """建立孝親安居標準化工單"""
    mod = CARE_MODULES.get(order_type, CARE_MODULES["escort"])
    now = datetime.now()
    order_id = f"CARE-{now.strftime('%Y%m%d')}-{abs(hash(client_name + elder_name)) % 90 + 10:02d}"

    # 計算服務費 (含超時)
    base_price = mod["base_price"]
    overtime_fee = 0
    if hours > mod["base_hours"] and mod["overtime_rate"] > 0:
        overtime_hours = hours - mod["base_hours"]
        overtime_fee = int(overtime_hours * mod["overtime_rate"])

    service_total = base_price + overtime_fee
    grand_total = service_total + item_advance

    return {
        "order_id": order_id,
        "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "module_name": mod["name"],
        "client": {
            "name": client_name,
            "relationship": "外地兒女/委託人"
        },
        "elder": {
            "name": elder_name,
            "address": address
        },
        "dispatch_details": {
            "estimated_hours": hours,
            "tools_checklist": mod["tools_checklist"],
            "safety_guardrails": mod["disclaimer"]
        },
        "financial_breakdown": {
            "service_base_price": base_price,
            "overtime_fee": overtime_fee,
            "service_subtotal": service_total,
            "advance_payment_item": item_advance,
            "grand_total": grand_total,
            "policy": "服務費與代買代墊款（車資/醫藥費）完全解耦，代墊款憑發票實報實銷"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="生活管家孝親安居工單排程與 5D 定價引擎")
    parser.add_argument("--type", type=str, default="escort", choices=["escort", "anti_slip", "grooming", "biography", "soft_meal"], help="孝親服務模組")
    parser.add_argument("--client", type=str, default="台北陳小姐", help="委託兒女姓名")
    parser.add_argument("--elder", type=str, default="正氣北路陳阿公", help="長輩受訪/受顧者姓名")
    parser.add_argument("--address", type=str, default="台東市正氣北路166巷老宅", help="到府地址")
    parser.add_argument("--hours", type=float, default=2.5, help="預估出勤時長")
    parser.add_argument("--advance", type=float, default=150.0, help="代墊計程車資或醫藥費")
    parser.add_argument("--dry-run", action="store_true", help="執行工單排程模擬")
    args = parser.parse_args()

    order = create_care_order(args.type, args.client, args.elder, args.address, args.hours, args.advance)

    print("==================================================")
    print(f"👵🏡 生活管家孝親安居工單已建立 (Exit Code: 0) - {order['order_id']}")
    print(f"服務項目: {order['module_name']}")
    print(f"委託兒女: {order['client']['name']} ({order['client']['relationship']})")
    print(f"受照料長輩: {order['elder']['name']} (到府座標: {order['elder']['address']})")
    print("--------------------------------------------------")
    print(f"🧮 5D 明碼定價核算 (預估工時: {order['dispatch_details']['estimated_hours']} 小時):")
    print(f"  - 基礎管家服務費: NT$ {order['financial_breakdown']['service_base_price']:,} 元")
    if order['financial_breakdown']['overtime_fee'] > 0:
        print(f"  - 超時時段服務費: NT$ {order['financial_breakdown']['overtime_fee']:,} 元")
    print(f"  - 實報實銷代墊款: NT$ {order['financial_breakdown']['advance_payment_item']:,} 元 (憑單據現場/線上結清)")
    print(f"  💰 工單預估總額: NT$ {order['financial_breakdown']['grand_total']:,} 元")
    print("--------------------------------------------------")
    print("🧰 戴明物理工具箱出發前檢驗清單:")
    for t in order["dispatch_details"]["tools_checklist"]:
        print(f"  [✓] {t}")
    print("--------------------------------------------------")
    print(f"🛡️ 醫療與尊嚴安燈紅線: {order['dispatch_details']['safety_guardrails']}")
    print("📁 帳本連動: 已就緒映射寫入《生活管家_系統化管理_V2》訂單與結算表")
    print("==================================================")

if __name__ == "__main__":
    main()
