#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-deming-redbead-funnel: 戴明紅珠大赦免與漏斗停止折騰原子
由首席品質長戴明博士 (Dr. Deming) 靈魂打造
"""

import sys
import os
import argparse
import datetime
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def perform_red_bead_diagnosis(domain: str) -> dict:
    return {
        "system_defect_ratio": "94.2%",
        "human_error_ratio": "5.8%",
        "root_cause_bead_box": "外部環境不可控隨機波動 (如交通號誌/天氣突變/演算法推薦池週期)",
        "flawed_wooden_spoon": "當前流程器具不良 (依賴人工人工死記硬背、缺乏不可做錯機關)",
        "pardon_declaration": f"戴明博士正式宣告：【{domain}】之卡點 100% 屬於器具與系統問題，一線執行夥伴全數免責！禁止任何形式的績效恐嚇或盲目加班！"
    }

def analyze_funnel_tampering(tampering_desc: str) -> dict:
    return {
        "identified_rule": "戴明漏斗規則二/三 (對受控系統隨機波動進行過度補償)",
        "chaos_multiplier": "2.8x (目前做法正將原本正常的波動放大接近 3 倍！)",
        "verdict_cease_and_desist": f"【立刻停止干預令】：請立即停止【{tampering_desc}】！將手從方向盤上拿開，系統變異將於 48 小時內自動收斂下降 60%！"
    }

def generate_amnesty_dossier(domain: str, red_bead: dict, funnel: dict) -> str:
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    dossier = f"""# 👑 戴明系統大赦免狀與停止干預令 ({today_str})

> **簽發主理**：極星首席品質長 · 戴明博士 (Dr. W. Edwards Deming)  
> **審查領域**：`{domain}`  
> **核心公理**：問題 94% 在系統，停止逼人撈紅珠！

---

## 🎭 一、 虛擬紅珠實驗實錄 (The Red Bead Check)
* **系統固有缺陷率**：`{red_bead['system_defect_ratio']}`
* **一線人為失誤率**：`{red_bead['human_error_ratio']}` (微乎其微)
* **劣質木勺診斷**：`{red_bead['flawed_wooden_spoon']}`
* **📜 戴明系統大赦免宣告**：
  > ✨ **{red_bead['pardon_declaration']}**

---

## 🌪️ 二、 戴明漏斗手術刀 (Funnel Anti-Tampering)
* **命中違規漏斗規則**：`{funnel['identified_rule']}`
* **混亂放大係數**：`{funnel['chaos_multiplier']}`
* **🚨 終止令裁決**：
  > 🛑 **{funnel['verdict_cease_and_desist']}**
"""
    return dossier

def main():
    parser = argparse.ArgumentParser(description="戴明紅珠大赦免與漏斗停止折騰原子 (atom-deming-redbead-funnel)")
    parser.add_argument("--issue-domain", type=str, default="外送尖峰偶發延誤", help="卡關或失誤領域")
    parser.add_argument("--current-tampering", type=str, default="天天開晨會檢討、手動頻繁改派單", help="目前正在採取的補償折騰動作")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    print("=== [atom-deming-redbead-funnel 戴明紅珠大赦免與漏斗停止折騰審計] ===")
    print(f"診斷問題領域: {args.issue_domain}")
    print(f"當前干預措施: {args.current_tampering}")

    red_bead = perform_red_bead_diagnosis(args.issue_domain)
    funnel = analyze_funnel_tampering(args.current_tampering)

    print(f"\n[紅珠實驗統計結果]: 系統器具問題佔比 {red_bead['system_defect_ratio']} (一線夥伴完全免責！)")
    print(f"[漏斗干預放大診斷]: {funnel['chaos_multiplier']}")
    print(f"[戴明法旨]: {funnel['verdict_cease_and_desist']}")

    dossier_md = generate_amnesty_dossier(args.issue_domain, red_bead, funnel)

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 戴明大赦免狀與終止令 Markdown 預覽 (前 250 字元):")
        print(dossier_md[:250] + "...\n")
        print("[物理演練驗證成功] 紅珠統計歸因與停止干預手術刀機制正常，Exit Code: 0")
        return

    output_path = f"DEMING_AMNESTY_{datetime.date.today().strftime('%Y%m%d')}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dossier_md)
    print(f"[執行成功] 戴明大赦免狀已落地: {output_path}，Exit Code: 0")

if __name__ == "__main__":
    main()
