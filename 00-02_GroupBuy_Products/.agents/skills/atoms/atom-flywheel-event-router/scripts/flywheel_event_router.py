#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/flywheel_event_router.py
全域業務事件意圖解析與流水線智慧路由引擎
專精於四大業務作戰動脈精準路由 (groupbuy / life_service / ai_education / forensics)
"""

import sys
import argparse
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')

# 四大業務動脈特徵字典與推薦下游專精原子
PIPELINE_DEFINITIONS = {
    "groupbuy": {
        "name": "管家選品與供應鏈流 (Groupbuy & SCM)",
        "keywords": ["商品", "生鮮", "魚", "肉", "腰果", "堅果", "高麗菜", "廠商報價", "進貨", "樣品", "規格", "包裝", "批發", "零售價", "大盤"],
        "downstream_atoms": [
            "atom-groupbuy-cost-auditor (供應鏈底價逆推與食安背調)",
            "atom-groupbuy-four-prism-copy (四大面向折射文案與商城規格)",
            "atom-poster-grid-architect (約瑟夫 12 欄視覺海報排版)",
            "atom-poster-print-andon (印刷出廠戴明十重安燈)"
        ]
    },
    "life_service": {
        "name": "生活管家與孝親安居流 (Senior Care & Living)",
        "keywords": ["長輩", "阿公", "阿嬤", "陪診", "看醫生", "馬偕", "防滑", "扶手", "配電盤", "修容", "理髮", "跑腿", "代買", "送餐", "雞湯", "外送", "到府"],
        "downstream_atoms": [
            "atom-pricing-5d-calculator (5D 勞務工時矩陣精算)",
            "atom-care-order-dispatcher (孝親派工單與裝備清單)",
            "atom-care-telehealth-card (外地兒女 3 分鐘安心聽診圖卡)",
            "atom-pricing-bulletproof-clause (防彈合約與高情商話術)"
        ]
    },
    "ai_education": {
        "name": "AI 實戰教育與工作坊流 (AI Education Workshop)",
        "keywords": ["開課", "工作坊", "教學", "實作", "課綱", "學員", "報名", "表單", "Google 日曆", "自備筆電", "軍事班", "教案", "投影片", "第講"],
        "downstream_atoms": [
            "atom-course-syllabus-scaffolder (每堂6席教案規格與10題表單)",
            "atom-course-enrollment-pipeline (正取6/備取2分流與24h-RSVP)",
            "atom-pricing-5d-calculator (5D-Asset 課程研發資產定價)"
        ]
    },
    "forensics": {
        "name": "商業調查與反欺詐徵信流 (Cyber Forensics & Recon)",
        "keywords": ["調查", "背調", "裁判書", "欺詐", "詐騙", "公司登記", "負責人", "判決", "案外人", "股權", "穿透", "信用", "黑名單"],
        "downstream_atoms": [
            "polaris-forensic-investigator (黑色調查與反欺詐穿透)",
            "atom-supplychain-tactical-negotiator (商業心理戰與對手預判)"
        ]
    }
}

def route_business_event(event_text: str) -> Dict[str, Any]:
    """解析事件文字意圖，計算信心分數並推薦路由"""
    scores = {}

    for pkey, pdata in PIPELINE_DEFINITIONS.items():
        matched = [k for k in pdata["keywords"] if k in event_text]
        # 簡單 TF 權重計分
        scores[pkey] = len(matched)

    best_pipeline = max(scores, key=scores.get)
    max_matches = scores[best_pipeline]

    # 計算置信度 (0.4 ~ 0.98)
    if max_matches == 0:
        best_pipeline = "groupbuy" # 預設 fallback
        confidence = 0.50
    else:
        confidence = min(0.98, round(0.65 + (max_matches * 0.08), 2))

    selected = PIPELINE_DEFINITIONS[best_pipeline]

    return {
        "status": "ROUTING_SUCCESS",
        "input_preview": event_text[:80] + "..." if len(event_text) > 80 else event_text,
        "selected_pipeline": best_pipeline,
        "pipeline_name": selected["name"],
        "confidence_score": confidence,
        "match_count": max_matches,
        "recommended_atomic_pipeline": selected["downstream_atoms"]
    }

def main():
    parser = argparse.ArgumentParser(description="全域業務事件意圖解析與流水線智慧路由引擎")
    parser.add_argument("--input", type=str, default="這款智利冷凍鮭魚廠商開盤每公斤 450 元，請幫我分析底價與文案", help="原始業務事件描述")
    parser.add_argument("--dry-run", action="store_true", help="執行事件路由模擬")
    args = parser.parse_args()

    res = route_business_event(args.input)

    print("==================================================")
    print(f"🧭 全域業務事件智慧路由完成 (Exit Code: 0)")
    print(f"輸入事件摘要: {res['input_preview']}")
    print("--------------------------------------------------")
    print(f"🎯 目標作戰動脈: 【{res['selected_pipeline']}】 -> {res['pipeline_name']}")
    print(f"📊 路由信心指數: {res['confidence_score'] * 100:.1f}% (特徵命中數: {res['match_count']})")
    print("--------------------------------------------------")
    print("🔗 下游專精原子調度鏈路 (Recommended Atomic Chain):")
    for idx, atom in enumerate(res["recommended_atomic_pipeline"], 1):
        print(f"  Step {idx}: {atom}")
    print("==================================================")

if __name__ == "__main__":
    main()
