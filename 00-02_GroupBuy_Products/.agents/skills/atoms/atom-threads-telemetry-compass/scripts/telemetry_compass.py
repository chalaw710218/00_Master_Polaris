#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
telemetry_compass.py
====================================================================
🧭 atom-threads-telemetry-compass Threads 數據遙測與指南針原子
首長：CTO 林納斯 ✕ 行銷長泰勒絲 ✕ 戴明博士
單一職責：發布後成效遙測、自帳回覆扣除真值互動率、四階破圈評級、時序快照。
====================================================================
"""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import Dict, Any, List

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "data")
INSIGHTS_FILE = os.path.join(DATA_DIR, "insights_history.jsonl")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def append_snapshot_history(records: List[Dict[str, Any]]):
    ensure_data_dir()
    now_iso = datetime.now().isoformat()
    with open(INSIGHTS_FILE, "a", encoding="utf-8") as f:
        for r in records:
            entry = {
                "snapshot_time": now_iso,
                "post_id": r["post_id"],
                "views": r["views"],
                "likes": r["likes"],
                "real_replies": r["real_replies"],
                "reposts": r["reposts"],
                "engagement_rate": r["engagement_rate"],
                "rating": r["rating"]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def calculate_rating(views: int, eng_rate: float) -> str:
    """計算四階評級"""
    if views >= 250:
        return "🏆 爆款 (Viral)"
    elif views >= 100:
        return "🚀 破圈 (Breakthrough)"
    elif eng_rate >= 5.0:
        return "💬 高互動 (High Resonance)"
    return "🌱 常民累積中 (Seeding)"

def fetch_telemetry_report(limit: int = 5, dry_run: bool = False) -> Dict[str, Any]:
    """獲取數據遙測儀表板"""
    # 模擬近期 5 篇真實貼文遙測數據（含自帳回覆校準）
    sample_posts_telemetry = [
        {
            "post_id": "th_20261113_001",
            "snippet": "入冬之後的台東夜晚，廚房那鍋滾沸的熱氣...",
            "views": 320,
            "likes": 28,
            "raw_replies": 8,
            "self_replies": 3, # 扣除自帳首回覆與回答
            "reposts": 4,
            "quotes": 1
        },
        {
            "post_id": "th_20261112_002",
            "snippet": "週一的開工打卡，是人類發明最違反生物本能的發明...",
            "views": 185,
            "likes": 19,
            "raw_replies": 6,
            "self_replies": 2,
            "reposts": 2,
            "quotes": 0
        },
        {
            "post_id": "th_20261111_003",
            "snippet": "看大家衝流量衝得這麼認真，生活管家默默在後排...",
            "views": 85,
            "likes": 12,
            "raw_replies": 4,
            "self_replies": 1,
            "reposts": 1,
            "quotes": 0
        }
    ]

    processed_posts = []
    for p in sample_posts_telemetry[:limit]:
        views = max(1, p["views"])
        real_replies = max(0, p["raw_replies"] - p["self_replies"])
        total_interactions = p["likes"] + real_replies + p["reposts"] + p["quotes"]
        eng_rate = round((total_interactions / views) * 100, 2)
        rating = calculate_rating(views, eng_rate)
        
        processed_posts.append({
            "post_id": p["post_id"],
            "snippet": p["snippet"],
            "views": views,
            "likes": p["likes"],
            "real_replies": real_replies,
            "self_replies_deducted": p["self_replies"],
            "reposts": p["reposts"],
            "quotes": p["quotes"],
            "real_total_interactions": total_interactions,
            "engagement_rate": eng_rate,
            "rating": rating
        })

    if not dry_run:
        append_snapshot_history(processed_posts)

    return {
        "status": "success",
        "atom": "atom-threads-telemetry-compass",
        "mode": "DRY_RUN" if dry_run else "PRODUCTION",
        "inspected_posts_count": len(processed_posts),
        "summary": {
            "total_views": sum(p["views"] for p in processed_posts),
            "total_likes": sum(p["likes"] for p in processed_posts),
            "average_engagement_rate": round(sum(p["engagement_rate"] for p in processed_posts) / max(1, len(processed_posts)), 2),
            "viral_count": sum(1 for p in processed_posts if "爆款" in p["rating"]),
            "breakthrough_count": sum(1 for p in processed_posts if "破圈" in p["rating"])
        },
        "posts": processed_posts,
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-telemetry-compass Threads 數據遙測原子")
    parser.add_argument("--limit", type=int, default=5, help="探索貼文數量")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬遙測")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = fetch_telemetry_report(limit=args.limit, dry_run=args.dry_run)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"數據遙測完成：平均真值互動率 {result['summary']['average_engagement_rate']}%")

    sys.exit(0)

if __name__ == "__main__":
    main()
