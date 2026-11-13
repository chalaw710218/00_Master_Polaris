#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rss_watcher.py
====================================================================
📡 atom-threads-rss-watcher Threads 友店公開增量巡邏哨兵
首長：生活管家影 ✕ CTO 林納斯
單一職責：台東在地友店動態巡邏、快取比對、增量新鮮貼文純淨萃取。
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
CACHE_FILE = os.path.join(DATA_DIR, "sentinel_cache.json")

DEFAULT_TARGET_SHOPS = [
    {"handle": "hungryyyummy", "name": "餓人工作室", "type": "街頭美食"},
    {"handle": "tsao_min", "name": "草民手作料理", "type": "慢食早午餐"},
    {"handle": "slowfoodtaitung", "name": "慢食台東", "type": "在地風土文化"},
    {"handle": "hattcoffee", "name": "薄荷巴黎咖啡", "type": "老宅咖啡甜點"}
]

# 模擬友店公開最新動態
SAMPLE_PUBLIC_POSTS = {
    "hungryyyummy": {
        "post_id": "th_post_hungry_088",
        "title": "今天台東風好大！我們連夜熬的大骨肉骨茶剛出爐，快來喝一碗避避風！",
        "permalink": "https://threads.net/@hungryyyummy/post/th_post_hungry_088",
        "published_at": "2026-11-13T17:40:00Z"
    },
    "tsao_min": {
        "post_id": "th_post_tsaomin_021",
        "title": "週五手作野莓酸種麵包！剛切開的氣孔很均勻，明天早晨限定販售。",
        "permalink": "https://threads.net/@tsao_min/post/th_post_tsaomin_021",
        "published_at": "2026-11-13T16:20:00Z"
    },
    "slowfoodtaitung": {
        "post_id": "th_post_slowfood_009",
        "title": "秋天的部落收成慶典，長輩們捧著紅藜與小米，這就是土地最真切的餽贈。",
        "permalink": "https://threads.net/@slowfoodtaitung/post/th_post_slowfood_009",
        "published_at": "2026-11-13T15:10:00Z"
    }
}

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def load_cache() -> Dict[str, str]:
    ensure_data_dir()
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_cache(cache_data: Dict[str, str]):
    ensure_data_dir()
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

def patrol_shops(targets: List[str] = None, dry_run: bool = False, reset_cache: bool = False) -> Dict[str, Any]:
    """巡邏核心函式"""
    ensure_data_dir()
    
    if reset_cache:
        save_cache({})
        cached_ids = {}
    else:
        cached_ids = load_cache()

    if not targets:
        target_list = [s["handle"] for s in DEFAULT_TARGET_SHOPS]
    else:
        target_list = targets

    fresh_findings = []
    
    for handle in target_list:
        if handle in SAMPLE_PUBLIC_POSTS:
            post = SAMPLE_PUBLIC_POSTS[handle]
            pid = post["post_id"]
            
            # 比對快取
            if cached_ids.get(handle) == pid and not dry_run:
                continue # 已讀過，略過
                
            finding = {
                "handle": handle,
                "post_id": pid,
                "title": post["title"],
                "permalink": post["permalink"],
                "published_at": post["published_at"],
                "discovered_at": datetime.now().isoformat(),
                "is_fresh": True
            }
            fresh_findings.append(finding)
            
            if not dry_run:
                cached_ids[handle] = pid

    if not dry_run and fresh_findings:
        save_cache(cached_ids)

    return {
        "status": "success",
        "atom": "atom-threads-rss-watcher",
        "mode": "DRY_RUN" if dry_run else "PRODUCTION",
        "targets_patrolled_count": len(target_list),
        "fresh_posts_found_count": len(fresh_findings),
        "fresh_posts": fresh_findings,
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-rss-watcher Threads 友店增量巡邏哨兵")
    parser.add_argument("--targets", type=str, default=None, help="逗號分隔之目標帳號名單")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬不更新快取")
    parser.add_argument("--reset-cache", action="store_true", default=False, help="重置已讀快取")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    targets = [t.strip() for t in args.targets.split(",")] if args.targets else None
    result = patrol_shops(targets=targets, dry_run=args.dry_run, reset_cache=args.reset_cache)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"巡邏完成：發現 {result['fresh_posts_found_count']} 則新鮮友店貼文。")

    sys.exit(0)

if __name__ == "__main__":
    main()
