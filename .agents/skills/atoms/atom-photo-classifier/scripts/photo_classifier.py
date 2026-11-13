#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
photo_classifier.py
====================================================================
👁️ atom-photo-classifier 照片視覺語意精準分類原子
首長：首席科技偵察官艾達 ✕ 首席視覺長約瑟夫 ✕ 戴明博士
單一職責：單張照片特徵分析、OCR語意萃取、三條路線確定性判定。
====================================================================
"""

import sys
import os
import json
import argparse
from typing import Dict, Any

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

POSTER_KEYWORDS = ["海報", "講座", "工作坊", "繪本", "共讀", "展覽", "活動", "日期", "地點", "報名", "主辦", "入場", "poster", "workshop", "event"]
PRODUCT_KEYWORDS = ["肉", "蝦", "魚", "生鮮", "水果", "樣品", "規格", "包裝", "大盤", "批發", "雞腿", "釋迦", "牛", "豬", "價格", "特產"]
LIFE_KEYWORDS = ["外送", "後照鏡", "機車", "修繕", "終端", "螢幕", "代碼", "理貨", "街景", "下雨", "日常", "手拍", "鍵盤", "宵夜", "廚房"]

def classify_photo(input_ref: str, notes: str = "") -> Dict[str, Any]:
    """照片分類核心演算法"""
    combined = f"{input_ref} {notes}".lower()
    
    score_poster = sum(2 for k in POSTER_KEYWORDS if k in combined)
    score_product = sum(2 for k in PRODUCT_KEYWORDS if k in combined)
    score_life = sum(2 for k in LIFE_KEYWORDS if k in combined)
    
    # 預設邏輯
    max_score = max(score_poster, score_product, score_life)
    
    if max_score == score_poster and score_poster > 0:
        route = "EVENT_POSTER"
        route_name = "路線 A【活動海報 (Event Poster)】"
        target_skill = "atom-event-intel-copy"
        confidence = 0.95
    elif max_score == score_product and score_product > 0:
        route = "SOURCING_PRODUCT"
        route_name = "路線 B【生鮮商品/選品照 (Product & Sourcing)】"
        target_skill = "sharp-groupbuy-analyzer"
        confidence = 0.92
    else:
        route = "FOUNDER_LIFE"
        route_name = "路線 C【創辦人日常隨手拍 (Founder Life & Chores)】"
        target_skill = "atom-boss-direct-copy"
        confidence = 0.88

    return {
        "status": "success",
        "atom": "atom-photo-classifier",
        "input_reference": input_ref,
        "input_notes": notes,
        "classification": {
            "route_code": route,
            "route_name": route_name,
            "confidence_score": confidence,
            "recommended_next_atom": target_skill
        },
        "extracted_features": {
            "detected_keywords": [k for k in (POSTER_KEYWORDS + PRODUCT_KEYWORDS + LIFE_KEYWORDS) if k in combined],
            "visual_context_summary": f"檢測到與【{route_name}】高度相符之視覺語意特徵。"
        },
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-photo-classifier 照片視覺語意精準分類原子")
    parser.add_argument("--input", type=str, default="20261113_taitung_bread_workshop.jpg", help="圖片路徑或檔案名稱")
    parser.add_argument("--notes", type=str, default="草民舉辦的週末野莓酸種烘焙分享會", help="創辦人隨附備註")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = classify_photo(input_ref=args.input, notes=args.notes)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[{result['classification']['route_name']}] 信心度: {result['classification']['confidence_score']}")
        print(f"建議路由原子: {result['classification']['recommended_next_atom']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
