#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-taylor-funnel-telemetry: 行銷轉化漏斗設計與共鳴遙測原子腳本
專職負責行銷長泰勒絲 (Taylor) 行銷四階獲客漏斗轉化率計算、共鳴遙測與防騷擾控管。
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def calculate_marketing_funnel(public_reach: int, bio_clicks: int, private_leads: int, orders: int) -> dict:
    """計算行銷四階漏斗各級轉化率"""
    safe_reach = max(1, public_reach)
    safe_clicks = max(1, bio_clicks)
    safe_leads = max(1, private_leads)

    cr_reach_to_bio = round((bio_clicks / safe_reach) * 100, 2)
    cr_bio_to_private = round((private_leads / safe_clicks) * 100, 2)
    cr_private_to_order = round((orders / safe_leads) * 100, 2)
    cr_overall = round((orders / safe_reach) * 100, 3)

    # 共鳴度評級
    if cr_private_to_order >= 20.0 and cr_reach_to_bio >= 5.0:
        resonance_grade = "S級 (深層信任共振 · 高LTV關係人口)"
    elif cr_private_to_order >= 10.0:
        resonance_grade = "A級 (健康穩態轉化 · 留存良好)"
    else:
        resonance_grade = "B級 (公域漏斗正常 · 需強化私域特權價值)"

    return {
        "funnel_metrics": {
            "stage_1_public_reach": public_reach,
            "stage_2_bio_clicks": bio_clicks,
            "stage_3_private_leads": private_leads,
            "stage_4_paid_orders": orders
        },
        "conversion_rates": {
            "reach_to_bio_pct": cr_reach_to_bio,
            "bio_to_private_pct": cr_bio_to_private,
            "private_to_order_pct": cr_private_to_order,
            "overall_end_to_end_pct": cr_overall
        },
        "resonance_grade": resonance_grade,
        "anti_fatigue_rule": "每週私域推播鎖定 1~2 則，封鎖率趨近 0.0%，杜絕噪音促銷！"
    }

def main():
    parser = argparse.ArgumentParser(description="行銷轉化漏斗設計與共鳴遙測原子")
    parser.add_argument("--public-reach", type=int, default=12000, help="公域曝光觸達數")
    parser.add_argument("--bio-clicks", type=int, default=960, help="個人主頁點擊數")
    parser.add_argument("--private-leads", type=int, default=320, help="私域客廳新進名單數")
    parser.add_argument("--orders", type=int, default=78, help="實體履約成交訂單數")
    parser.add_argument("--broadcasts-per-week", type=int, default=2, help="每週私域推播次數")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    print("=== [atom-taylor-funnel-telemetry] 行銷長泰勒絲 · 四階獲客漏斗遙測 ===")
    res = calculate_marketing_funnel(
        public_reach=args.public_reach,
        bio_clicks=args.bio_clicks,
        private_leads=args.private_leads,
        orders=args.orders
    )

    print("\n📊 **【四階行銷漏斗轉化數據】**")
    print(f"  1. 公域微動態觸達 (Stage 1): {res['funnel_metrics']['stage_1_public_reach']} 人")
    print(f"  2. 主頁接梗引流 (Stage 2): {res['funnel_metrics']['stage_2_bio_clicks']} 次 (點擊率: {res['conversion_rates']['reach_to_bio_pct']}%)")
    print(f"  3. 私域客廳沉澱 (Stage 3): {res['funnel_metrics']['stage_3_private_leads']} 名 (轉化率: {res['conversion_rates']['bio_to_private_pct']}%)")
    print(f"  4. 實體履約付費 (Stage 4): {res['funnel_metrics']['stage_4_paid_orders']} 筆 (成交率: {res['conversion_rates']['private_to_order_pct']}%)")
    print(f"  * 全鏈路端對端轉化率: {res['conversion_rates']['overall_end_to_end_pct']}%")

    print(f"\n受眾情緒共鳴度評級: 【{res['resonance_grade']}】")
    print(f"防疲憊推播控管: 每週 {args.broadcasts_per_week} 則 ➔ {'[合規 安全範圍]' if args.broadcasts_per_week <= 2 else '[警告 超過2則恐引發封鎖！]'}")

    print("\n[+] 行銷轉化漏斗與共鳴遙測完成 (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
