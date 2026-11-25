#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
munger_inversion_veto.py - 查理·蒙格逆向致死缺陷一票否決引擎
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

def audit_failure_modes(item: dict) -> dict:
    """審計五大逆向致死缺陷"""
    name = item.get("item_name", "未命名品項")
    drip_loss = item.get("drip_loss_rate", 0.0)
    has_bones = item.get("has_pin_bones", False)
    bone_safeguard = item.get("bone_removal_safeguard", False)
    prep_mins = item.get("kitchen_prep_minutes", 10)
    has_recipe_card = item.get("has_quick_recipe_card", False)
    dsi_days = item.get("projected_dsi_days", 5)
    margin = item.get("contribution_margin", 0.0)
    is_rare = item.get("is_rare_item", False)
    
    fatal_defects = []
    
    # 缺陷 1: 解凍失水率 > 2%
    if drip_loss > 0.02:
        fatal_defects.append(f"解凍失水率高達 {drip_loss:.1%} (上限 2.0%)，肉質將嚴重乾柴！")
        
    # 缺陷 2: 多刺風險且無防呆
    if has_bones and not bone_safeguard:
        fatal_defects.append("存在細刺卡喉風險且未進行專業去刺處理，易引發客訴！")
        
    # 缺陷 3: 料理手續過繁 (>15分且無簡化圖卡)
    if prep_mins > 15 and not has_recipe_card:
        fatal_defects.append(f"備料料理耗時 {prep_mins} 分鐘且無極簡懶人圖卡食譜，顧客回購意願低！")
        
    # 缺陷 4: 庫存週轉天數 DSI > 15 天
    if dsi_days > 15:
        fatal_defects.append(f"預估庫存天數 {dsi_days} 天超過 15 天死線，將吞噬冷凍電費與流動性！")
        
    # 缺陷 5: 邊際貢獻率不足
    min_margin = 0.45 if is_rare else 0.30
    if margin < min_margin:
        fatal_defects.append(f"邊際貢獻率 {margin:.1%} 低於底線 {min_margin:.0%} (孤品需45%，常態品需30%)！")
        
    is_passed = len(fatal_defects) == 0
    verdict = (
        "✅ 逆向審查全數通過！具備物理防呆，准予採購發行！"
        if is_passed else
        f"❌ 查理·蒙格一票否決！偵測到 {len(fatal_defects)} 項未解決的致死缺陷，禁止上架！"
    )

    return {
        "item_name": name,
        "is_passed": is_passed,
        "fatal_defects_count": len(fatal_defects),
        "fatal_defects": fatal_defects,
        "munger_inversion_verdict": verdict
    }

def main():
    parser = argparse.ArgumentParser(description="查理·蒙格逆向致死缺陷一票否決引擎")
    parser.add_argument("--audit", type=str, required=True, help="受檢商品資料 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.audit)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = audit_failure_modes(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
