#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-taylor-campaign-launchpad: 行銷活動策劃、選品攻堅與全域發射原子腳本
專職負責行銷長泰勒絲 (Taylor) 商業行銷戰役全案策劃與四階段行銷檔期推進。
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

def plan_marketing_campaign(campaign_name: str, product: str, target_audience: str) -> dict:
    """生成全域商業行銷戰役企劃藍圖"""
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 四階段行銷戰役推進
    phases = [
        {
            "phase": "Phase 1: 痛點預熱 (Teaser)",
            "duration": "Day 1 ~ Day 2",
            "objective": "同理受眾深層焦慮，引發好奇，絕不提早叫賣商品",
            "copy_angle": f"描摹【{target_audience}】每天面對的具體生活摩擦與疲憊，激發情感共鳴",
            "channels": ["Threads (喵編生活隨筆)", "FB (日常情境長文)"]
        },
        {
            "phase": "Phase 2: 價值發射 (Value Launch)",
            "duration": "Day 3 ~ Day 5",
            "objective": f"正式揭示【{product}】，確立第一性物理真值與無可比擬的解決方案",
            "copy_angle": "0.0%包冰、手指逆紋摸刺三次、透明跑腿費、產地直達，粉碎市場一切灰色黑洞",
            "channels": ["FB (專業深度選品文)", "LINE OA (VIP 優先認領通知)", "實體友店 (A3 網格海報)"]
        },
        {
            "phase": "Phase 3: 常民證言 (Social Proof)",
            "duration": "Day 6 ~ Day 7",
            "objective": "釋放真實常民廚房故事與掌廚者自豪，形成朋友圈口碑轉發",
            "copy_angle": "挑食小朋友把盤底吃光、老長輩安心大口嚼魚排的真實生活切片",
            "channels": ["Threads (短影音與顧客留言截圖)", "FB (常民心聲口述)"]
        },
        {
            "phase": "Phase 4: 誠懇收口 (Honest Close)",
            "duration": "Day 8",
            "objective": "以客觀物理稀缺性誠懇收單，杜絕農場恐嚇倒數",
            "copy_angle": "產地單日僅捕獲限定配額、每堂課嚴格限額 6 席手把手教學，最後保留席認領",
            "channels": ["LINE OA (最後配額私域提醒)", "Threads (喵編收工打烊隨筆)"]
        }
    ]

    uvp = f"以純粹商人信譽與真實風土品質，為【{target_audience}】徹底解決【{product}】領域的痛點！"

    return {
        "campaign_name": campaign_name,
        "product_service": product,
        "target_audience": target_audience,
        "planned_date": today_str,
        "unique_value_proposition": uvp,
        "phases": phases,
        "status": "CAMPAIGN_PLANNED_SUCCESS"
    }

def main():
    parser = argparse.ArgumentParser(description="行銷活動策劃、選品攻堅與全域發射原子")
    parser.add_argument("--campaign-name", type=str, default="成功港冬季高脂午仔魚現流上市", help="行銷活動名稱")
    parser.add_argument("--product", type=str, default="成功港急凍午仔魚", help="核心商品或服務")
    parser.add_argument("--target-audience", type=str, default="雙薪家庭掌廚媽媽", help="目標受眾描摹")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    print("=== [atom-taylor-campaign-launchpad] 行銷長泰勒絲 · 行銷活動全案策劃 ===")
    res = plan_marketing_campaign(args.campaign_name, args.product, args.target_audience)

    print(f"\n戰役名稱: 『{res['campaign_name']}』")
    print(f"核心商品: {res['product_service']} | 目標受眾: {res['target_audience']}")
    print(f"核心價值主張 (UVP): {res['unique_value_proposition']}")

    print("\n🚀 **【泰勒絲行銷戰役四大推進檔期】**")
    for p in res["phases"]:
        channels_str = ", ".join(p["channels"])
        print(f"\n* 【{p['phase']}】({p['duration']})")
        print(f"  - 戰略目標: {p['objective']}")
        print(f"  - 文案主切角: {p['copy_angle']}")
        print(f"  - 傳播渠道: [{channels_str}]")

    print("\n[+] 全域商業行銷戰役企劃裝配完成 (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
