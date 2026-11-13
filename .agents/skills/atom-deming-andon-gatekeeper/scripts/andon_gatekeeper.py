#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
andon_gatekeeper.py - 戴明全域安燈天網與90分致命紅線質檢引擎
版權所有 (c) 2026 極星內閣 - 首席品質長戴明 (Dr. Deming)
"""

import sys
import json
import argparse
import re

# 促銷賤詞庫（嚴禁出現在對外官方文案）
CHEAP_BARGAIN_WORDS = [
    "團購", "便宜", "cp值", "破盤", "清倉", "跳樓大拍賣", "撿便宜", "俗俗賣", "買一送一狂歡", "低價甩賣"
]

# 內部研發機密詞（絕對零洩漏）
BRAND_LEAK_WORDS = [
    "極星", "polaris", "master_polaris"
]

def audit_zone_a(payload: dict) -> dict:
    """審計防區 A: 5D 定價與財務風控"""
    violations = []
    score = 100
    
    labor_fee = payload.get("labor_fee", 0)
    advance_payment = payload.get("advance_payment", 0)
    advance_confirmed = payload.get("advance_confirmed", False)
    gross_margin = payload.get("gross_margin", 0.0)
    
    # REDLINE_A1: 勞務與代墊未分離
    if "labor_fee" not in payload or "advance_payment" not in payload:
        violations.append("REDLINE_A1: 勞務服務費與採購代墊款未做分離標示")
        score -= 50
        
    # REDLINE_A2: 代墊無知情前置確認
    if advance_payment > 0 and not advance_confirmed:
        violations.append("REDLINE_A2: 代墊款缺乏創辦人或客戶知情前置確認")
        score -= 40
        
    # REDLINE_A3: 代墊款 > 3000 且未收定金
    deposit_collected = payload.get("deposit_collected", False)
    if advance_payment > 3000 and not deposit_collected:
        violations.append(f"REDLINE_A3: 單筆代墊款 (NT$ {advance_payment}) 超過 3,000 元且未收取定金")
        score -= 30
        
    # REDLINE_A4: 負毛利阻斷
    if gross_margin < 0:
        violations.append(f"REDLINE_A4: 負毛利出勤阻斷 (毛利率: {gross_margin:.1%})")
        score -= 50
    elif gross_margin < 0.20:
        # 低於 20% 毛利扣分警告
        score -= 15
        
    return {
        "zone": "A_5D_PRICING",
        "score": max(0, score),
        "violations": violations,
        "is_passed": len(violations) == 0 and score >= 90
    }

def audit_zone_b(payload: dict) -> dict:
    """審計防區 B: 社群選品與品牌防禦"""
    violations = []
    score = 100
    text = payload.get("text", "")
    has_sample = payload.get("has_sample_photo", False)
    text_lower = text.lower()
    
    # REDLINE_B1: 品牌代號洩漏
    for leak in BRAND_LEAK_WORDS:
        if leak in text_lower:
            violations.append(f"REDLINE_B1: 偵測到對外洩漏內部代號 '{leak}'！觸犯法定零洩漏防火牆！")
            score -= 100
            
    # REDLINE_B2: 促銷賤詞
    found_cheap = [w for w in CHEAP_BARGAIN_WORDS if w in text_lower]
    if found_cheap:
        violations.append(f"REDLINE_B2: 偵測到低階促銷賤詞: {found_cheap}，嚴重破壞生活管家高端信譽！")
        score -= (len(found_cheap) * 25)
        
    # REDLINE_B3: 現場打樣實拍
    if not has_sample:
        violations.append("REDLINE_B3: 缺乏真實產地或現場打樣樣品證明")
        score -= 20
        
    # 檢查字數與敷衍程度
    if len(text.strip()) < 15:
        score -= 15
        
    return {
        "zone": "B_SOCIAL_PRODUCT",
        "score": max(0, score),
        "violations": violations,
        "is_passed": len(violations) == 0 and score >= 90
    }

def audit_zone_c(payload: dict) -> dict:
    """審計防區 C: 代碼與日結平帳"""
    violations = []
    score = 100
    
    exit_code = payload.get("exit_code", 0)
    encoding = payload.get("encoding", "").lower()
    balance_diff = payload.get("balance_diff", 0)
    has_hardcoded_secrets = payload.get("has_hardcoded_secrets", False)
    
    # REDLINE_C1: Exit Code != 0
    if exit_code != 0:
        violations.append(f"REDLINE_C1: 代碼執行未通過物理驗證 (Exit Code: {exit_code})")
        score -= 100
        
    # REDLINE_C2: 編碼非 UTF-8
    if encoding and encoding != "utf-8":
        violations.append(f"REDLINE_C2: 檔案編碼為 '{encoding}'，非強制 utf-8，Windows 環境易發亂碼崩潰")
        score -= 30
        
    # REDLINE_C3: 日結平帳差額不為 0
    if balance_diff != 0:
        violations.append(f"REDLINE_C3: 營業日結借貸不平帳，差額 NT$ {balance_diff}，戴明原則一元不差")
        score -= 40
        
    # REDLINE_C4: 硬編碼私鑰
    if has_hardcoded_secrets:
        violations.append("REDLINE_C4: 偵測到硬編碼 API Token 或私鑰，嚴重資安違規")
        score -= 100
        
    return {
        "zone": "C_CODE_SETTLEMENT",
        "score": max(0, score),
        "violations": violations,
        "is_passed": len(violations) == 0 and score >= 90
    }

def main():
    parser = argparse.ArgumentParser(description="戴明安燈天網質檢引擎")
    parser.add_argument("--zone", choices=["A", "B", "C"], required=True, help="受檢防區 (A: 5D報價, B: 社群選品, C: 代碼平帳)")
    parser.add_argument("--payload", type=str, required=True, help="受檢資料 (JSON 字串)")
    parser.add_argument("--strict-exit", action="store_true", help="若未通過則以 exit code 1 阻斷退出")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.payload)
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    if args.zone == "A":
        res = audit_zone_a(data)
    elif args.zone == "B":
        res = audit_zone_b(data)
    else:
        res = audit_zone_c(data)
        
    print(json.dumps(res, ensure_ascii=False, indent=2))
    
    if args.strict_exit and not res["is_passed"]:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
