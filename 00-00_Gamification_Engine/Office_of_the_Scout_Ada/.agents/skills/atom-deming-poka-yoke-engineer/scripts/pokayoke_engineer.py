#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pokayoke_engineer.py - 戴明神級防呆工坊與局部留置隔離引擎
版權所有 (c) 2026 極星內閣 - 首席品質長戴明 (Dr. Deming)
"""

import sys
import json
import argparse
import re

def normalize_taiwan_phone(phone_raw: str) -> tuple[str, bool]:
    """防呆自癒: 將各種台灣手機號碼格式標準化為 E.164 (+8869xxxxxxxx)"""
    cleaned = re.sub(r"[\s\-\(\)]", "", str(phone_raw))
    if cleaned.startswith("+886"):
        cleaned = "0" + cleaned[4:]
    elif cleaned.startswith("886"):
        cleaned = "0" + cleaned[3:]
        
    if re.match(r"^09\d{8}$", cleaned):
        e164 = "+886" + cleaned[1:]
        return e164, True
    return str(phone_raw), False

def process_pokayoke_batch(items: list) -> dict:
    """執行批次防呆自癒與留置隔離"""
    clean_stream = []
    quarantined = []
    healed_count = 0
    
    for idx, item in enumerate(items):
        item_id = item.get("id", f"ITEM_{idx+1}")
        reasons = []
        is_healed = False
        healed_item = dict(item)
        
        # 1. 字串防呆自癒 (去除首尾空格)
        for k, v in healed_item.items():
            if isinstance(v, str):
                trimmed = v.strip()
                if trimmed != v:
                    healed_item[k] = trimmed
                    is_healed = True
                    
        # 2. 金額數值防呆 (固定數值工法)
        amount = healed_item.get("amount")
        if amount is None or not isinstance(amount, (int, float)):
            reasons.append("金額缺失或非數值型別")
        elif amount <= 0:
            reasons.append(f"金額非正數 (amount={amount})，違反交易防線")
            
        # 3. 電話號碼防呆自癒 (接觸式工法)
        phone = healed_item.get("phone")
        if not phone:
            reasons.append("缺少收件人聯絡電話")
        else:
            norm_phone, ok = normalize_taiwan_phone(phone)
            if ok:
                if norm_phone != phone:
                    healed_item["phone"] = norm_phone
                    healed_item["_phone_self_healed"] = True
                    is_healed = True
            else:
                reasons.append(f"電話號碼格式無效無法自癒 ({phone})")
                
        # 4. 決策分流: 留置隔離 vs 放行進入合格流水線
        if reasons:
            quarantined.append({
                "item_id": item_id,
                "raw_item": item,
                "reasons": reasons,
                "quarantine_timestamp": "ACTIVE"
            })
        else:
            if is_healed:
                healed_count += 1
            clean_stream.append(healed_item)
            
    total = len(items)
    passed = len(clean_stream)
    quarantine_count = len(quarantined)
    
    return {
        "summary": {
            "total_items": total,
            "passed_clean": passed,
            "self_healed": healed_count,
            "quarantined": quarantine_count,
            "pipeline_yield_rate": f"{(passed / total * 100):.1f}%" if total > 0 else "0%"
        },
        "clean_stream": clean_stream,
        "quarantined_items": quarantined,
        "andon_status": "NORMAL" if quarantine_count == 0 else "QUARANTINE_ACTIVE"
    }

def main():
    parser = argparse.ArgumentParser(description="戴明防呆自癒與留置隔離引擎")
    parser.add_argument("--input-json", type=str, required=True, help="受檢批次資料 (JSON 陣列字串)")
    
    args = parser.parse_args()
    try:
        items = json.loads(args.input_json)
        if not isinstance(items, list):
            items = [items]
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    result = process_pokayoke_batch(items)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
