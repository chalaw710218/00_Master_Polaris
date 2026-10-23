#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polaris 5D AI Pricing Hub - CLI Quick Interpreter
路徑: 00-03_Brand_LifeButler/00-03-07_5D_AI_Pricing_Hub/scripts/run_interpret.py
作者: 工程長林納斯 (Linus) & 執行長雪 (Yuki)

使用方式：
1. 直接執行讀取預設輸入檔：
   python run_interpret.py
2. 傳入自訂文字：
   python run_interpret.py --text "公車總站拿都蘭便當，金額2400元"
"""

import sys
import os
import re
import argparse
from pathlib import Path

# Windows UTF-8 Console Setup
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 引入 5D 確定性演算法核心
SCRIPT_DIR = Path(__file__).resolve().parent
HUB_DIR = SCRIPT_DIR.parent
ROOT_DIR = HUB_DIR.parent.parent
ENGINE_DIR = ROOT_DIR / "00-00_Gamification_Engine"

if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

try:
    from polaris_5d_pricing_engine import Polaris5DPricingEngine
except ImportError:
    print(f"❌ 錯誤：找不到 polaris_5d_pricing_engine.py 於 {ENGINE_DIR}")
    sys.exit(1)


def parse_task_text(text: str) -> dict:
    """
    輕量語意關鍵字解碼器 (Semantic Decoder)
    從客人口語委託中提煉初步 5D 參數，供 5D 引擎精算
    """
    params = {
        "base_minutes": 35.0,
        "d1_friction": 1.0,
        "d2_difficulty": 1.0,
        "d3_degree": 1.0,
        "d4_development": 1.0,
        "d5_delight": 1.1,
        "item_value": 0.0,
        "advance_payment": 0.0,
        "is_urgent": False,
        "task_name": "生活管家即時委託",
        "recipient_info": "收件人"
    }

    t = text.lower()

    # 1. 金額解析 (例如 2400元, 2,400)
    money_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*元', text)
    if money_match:
        val_str = money_match.group(1).replace(',', '')
        val = float(val_str)
        params["item_value"] = val
        if "代墊" in text or "先付" in text or "付給" in text or val >= 500:
            params["advance_payment"] = val

    # 2. 跨運具 / 公車總站
    if "公車" in text or "總站" in text or "客運" in text or "火車站" in text or "鼎東" in text:
        params["d1_friction"] = 1.5
        params["task_name"] = "跨運具站台代收直送"
        params["d5_delight"] = 1.1

    # 3. 藥品 / 醫療 / 諮詢
    if "藥" in text or "診所" in text or "醫院" in text or "扭傷" in text or "看診" in text:
        params["d3_degree"] = 1.1
        params["task_name"] = "專業藥品諮詢與代買配送"
        params["d5_delight"] = 1.2

    # 4. 急件 / 臨時插單
    if "急" in text or "立刻" in text or "馬上" in text or "臨時" in text or "剛上車" in text or "快到了" in text:
        params["is_urgent"] = True
        params["d4_development"] = 1.6
        params["d5_delight"] = 1.2
        params["task_name"] = "當日緊急調度專車急件"

    # 5. 高價品判定
    if params["item_value"] >= 2000:
        params["d2_difficulty"] = 1.5
        if not params["is_urgent"]:
            params["task_name"] = "高價值商品安全護運專車直送"

    # 6. 人名提取
    name_match = re.search(r'([陳林黃張李王吳許鄭劉蔡謝洪金郭][先生|小姐|老爺|太太|女士|同學|長輩]*)', text)
    if name_match:
        params["recipient_info"] = name_match.group(1)

    return params


def main():
    parser = argparse.ArgumentParser(description="北極星 5D 價值精算 AI 快速判讀工具")
    parser.add_argument("--text", "-t", type=str, help="委託人原始口語訊息文字")
    parser.add_argument("--file", "-f", type=str, help="讀取的文字檔路徑")
    args = parser.parse_args()

    input_text = ""
    if args.text:
        input_text = args.text
    elif args.file:
        file_path = Path(args.file)
        if file_path.exists():
            input_text = file_path.read_text(encoding="utf-8")
    else:
        default_file = HUB_DIR / "input_task.txt"
        if default_file.exists():
            raw_lines = default_file.read_text(encoding="utf-8").splitlines()
            valid_lines = [l for l in raw_lines if not l.strip().startswith("#")]
            input_text = "\n".join(valid_lines).strip()

    if not input_text:
        print("💡 請在 input_task.txt 輸入客人的原始委託文字，或使用 --text \"...\" 參數執行！")
        print("示範案例：'幫我去公車總站拿都蘭下來的便當，總共2400元需要代墊，送給許先生'")
        sys.exit(0)

    print("==================================================")
    print("🤖 【5D AI 價值精算裁判長】啟動語意解析與防彈精算")
    print("==================================================")
    print(f"\n📩 客戶原始輸入：\n「{input_text}」\n")

    # 語意參數提煉
    extracted = parse_task_text(input_text)

    # 呼叫 5D 確定性演算法
    engine = Polaris5DPricingEngine(base_rate=250.0)
    res = engine.calculate(
        base_minutes=extracted["base_minutes"],
        d1_friction=extracted["d1_friction"],
        d2_difficulty=extracted["d2_difficulty"],
        d3_degree=extracted["d3_degree"],
        d4_development=extracted["d4_development"],
        d5_delight=extracted["d5_delight"],
        item_value=extracted["item_value"],
        advance_payment=extracted["advance_payment"],
        is_urgent=extracted["is_urgent"],
        task_name=extracted["task_name"],
        recipient_info=extracted["recipient_info"]
    )

    # 輸出結構化裁判報告
    print("--------------------------------------------------")
    print(f"📊 任務判定：{res['task_name']}")
    print(f"⏱️ 基礎工時：{res['metrics']['base_hours']} hr ({int(extracted['base_minutes'])} 分鐘)")
    print(f"📐 5D 矩陣係數：D1={extracted['d1_friction']} | D2={res['inputs']['d2_difficulty']} | D3={extracted['d3_degree']} | D4={res['inputs']['d4_development']} | D5={extracted['d5_delight']}")
    print(f"🌟 TP (時間點數)：{res['metrics']['tp_score']} TP")
    print(f"💰 建議定價：NT$ {res['final_price']} 元 (時薪基準 NT$ {int(res['metrics']['base_rate'])})")
    print(f"🚦 代墊款風控：[{res['advance_risk']['level']}] {res['advance_risk']['label']}")
    print(f"   ↳ 指引：{res['advance_risk']['instruction']}")
    print("--------------------------------------------------")
    print("🛡️ 防彈四大鐵律檢核：")
    for r in res["rules_enforced"]:
        print(f"  • {r}")
    print("--------------------------------------------------")
    print("\n💬 【一鍵複製對客話術（兼具防禦與泰勒絲人文溫度）】：")
    print(res["customer_script"])
    print("\n==================================================")


if __name__ == '__main__':
    main()
