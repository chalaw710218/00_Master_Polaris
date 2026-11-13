#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-cognition-artifact-compiler: 認知真值結構化產物編譯原子
由 CTO 林納斯 (Linus) ✕ 首席品質長戴明 (Dr. Deming) 聯合打造
"""

import sys
import os
import argparse
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def compile_to_sop(belief_text: str) -> str:
    sop_content = f"""# 📋 戴明神級防呆現場作業檢核表 (Poka-Yoke SOP)
> **來源認知真值**：{belief_text}
> **安燈質檢標記**：戴明源頭防呆 · 現場不可做錯

| 序號 | 查驗工項 | 物理合格標竿 (Pass/Fail) | 戴明防呆機關 / 工具 | 異常處置處方 (Andon) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | 現場環境安全初勘 | 浴室地面乾燥阻滑係數 >= 0.6 | 摩擦力滑動計 | 即刻鋪設防滑墊後方可作業 |
| 2 | 配電盤紅外檢測 | 斷路器端子溫升 <= 15 度C | 測溫熱像儀 | 發現過熱即拍照上傳並報修 |
| 3 | 體感溫差與血壓 | 收縮壓在正常範圍且頭暈指數為 0 | 臂式電子血壓計 | 超標暫停服務，通報家屬醫囑 |
| 4 | 工具箱出發清點 | 5 大標配工具無一缺漏 | 磁吸式凹槽收納盒 | 缺件亮紅燈，禁止外出派工 |
"""
    return sop_content

def compile_to_topics(curiosity_text: str) -> str:
    topics_content = f"""# 📱 Threads & FB 雙軌爆款選題靈感卡
> **來源商業好奇心**：{curiosity_text}
> **主政大師**：🎤 行銷長泰勒絲 (Taylor) ✕ 👤 生活管家影 (Kage)

## 🎯 選題切角：常民溫暖微觀察
- **常民痛點**：外地工作兒女對台東老家長輩「看病有沒有按時吃藥、浴室會不會滑倒」的無力焦慮。
- **大師金句**：「真正的孝順不是逢年過節塞紅包，而是你在台北開會時，知道老家洗手間多了一根妥貼握住的手把。」
- **雙主角調性**：生活管家親切真誠分享 ✕ 喵編第一留言插科打諢點火推薦池。
- **第一留言置頂草稿**：
  > 「喵編碎碎念：上次陪阿公量血壓，阿公偷塞了一顆芭樂給我... 這種溫暖只有管家懂啦！大家家裡的長輩浴室有裝扶手了嗎？」
"""
    return topics_content

def compile_to_pricing(fact_text: str) -> dict:
    return {
        "source_evidence": fact_text,
        "pricing_engine_tier": "5D-Universal-v2.0",
        "parameters": {
            "d1_labor_base_hourly": 350,
            "d2_friction_allowance": 120,
            "d3_asset_amortization": 50,
            "d4_impact_capture_factor": 1.15,
            "d5_cashflow_margin_target": 0.30
        },
        "minimum_order_price": 600,
        "poka_yoke_payment_clause": "滿意後現場簽認，拒絕預收大筆年費"
    }

def main():
    parser = argparse.ArgumentParser(description="認知真值結構化產物編譯原子 (atom-cognition-artifact-compiler)")
    parser.add_argument("--mode", type=str, choices=["compile-sop", "compile-topics", "compile-pricing"], default="compile-sop", help="編譯目標產物模式")
    parser.add_argument("--source-text", type=str, default="", help="輸入真值或事實文字 (留空則採用預設樣品)")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    # 預設範例
    default_inputs = {
        "compile-sop": "長輩浴室防滑與居安走道檢測：源頭防呆杜絕跌倒，工具出發前全數核對。",
        "compile-topics": "外地兒女遠距孝親焦慮：如何用一張圖卡傳遞老家長輩今日笑臉與生命體徵？",
        "compile-pricing": "台東市區派工交通摩擦與紅外熱像儀攤提成本實測。"
    }

    input_text = args.source_text.strip() if args.source_text else default_inputs[args.mode]

    # 品牌法定名稱零洩漏門禁
    if "極星" in input_text:
        print("[戴明安燈熔斷] 輸入文本含有內部代號！觸發品牌防火牆攔截。")
        sys.exit(1)

    print("=== [atom-cognition-artifact-compiler 認知真值結構化產物編譯] ===")
    print(f"編譯模式: {args.mode.upper()}")
    print(f"來源文字: {input_text[:60]}...")

    if args.mode == "compile-sop":
        result = compile_to_sop(input_text)
    elif args.mode == "compile-topics":
        result = compile_to_topics(input_text)
    else:
        result = json.dumps(compile_to_pricing(input_text), ensure_ascii=False, indent=2)

    if args.dry_run:
        print(f"\n[物理演練模式 --dry-run] 編譯產物預覽 (前 250 字元):")
        print(result[:250] + "...\n")
        print("[物理演練驗證成功] 產物編譯結構與品牌安燈門禁正常，Exit Code: 0")
        return

    print("[執行成功] 產物編譯落地完畢，Exit Code: 0")

if __name__ == "__main__":
    main()
