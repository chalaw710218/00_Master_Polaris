#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neighbor_crm.py
====================================================================
🤝 atom-threads-neighbor-crm 在地友店聯盟與登門回禮原子
首長：生活管家影 ✕ CTO 林納斯
單一職責：185 家友店巡邏、看見苦心走心留言、常客回禮、好友帳本沉澱。
====================================================================
"""

import sys
import os
import json
import random
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
FRIENDS_FILE = os.path.join(DATA_DIR, "friend_interactions.json")

SAMPLE_LOCAL_SHOPS = [
    {"handle": "hattcoffee", "name": "薄荷巴黎咖啡", "category": "咖啡甜點", "vibe": "老宅慢步調"},
    {"handle": "howhow_sweets", "name": "好厚甜點工作室", "category": "烘焙", "vibe": "手工派皮堅持"},
    {"handle": "shuramen", "name": "修拉麵", "category": "日式拉麵", "vibe": "濃醇豚骨大骨熬煮"},
    {"handle": "tiehua_craft", "name": "鐵花手作生活", "category": "原民工藝", "vibe": "月桃編織傳承"},
    {"handle": "tsaomin_bread", "name": "草民手作麵包", "category": "野生酵母麵包", "vibe": "天然發酵氣孔"},
    {"handle": "travel_zztaitung", "name": "走走池上", "category": "在地選品", "vibe": "稻浪與慢讀"}
]

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(FRIENDS_FILE):
        initial_db = {
            "last_updated": datetime.now().isoformat(),
            "total_friends_count": len(SAMPLE_LOCAL_SHOPS),
            "interactions": {
                shop["handle"]: {
                    "name": shop["name"],
                    "category": shop["category"],
                    "visits_count": 0,
                    "relationship_tier": "LEVEL_1_NEIGHBOR",
                    "last_visited": None
                } for shop in SAMPLE_LOCAL_SHOPS
            }
        }
        with open(FRIENDS_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_db, f, ensure_ascii=False, indent=2)

def generate_artisan_praise(shop: Dict[str, str]) -> str:
    """生成看見店家苦心的走心讚美"""
    cat = shop.get("category", "")
    if "烘焙" in cat or "麵包" in cat:
        return f"@{shop['handle']} 光看麵團烤出來的裂紋與發酵氣孔，就知道師傅清晨四點的汗水有多扎實。台東有你們在，早晨很幸福。🌾"
    elif "咖啡" in cat:
        return f"@{shop['handle']} 木質吧台飄出來的淺焙香氣，總是能把一整天的浮躁安靜接住。生活管家默默在角落為你們鼓掌。☕"
    elif "拉麵" in cat or "小吃" in cat:
        return f"@{shop['handle']} 真正深層的湯頭是時間熬出來的，騙不了舌頭。謝謝你們在大街小巷裡守著這份熱氣。🍜"
    else:
        return f"@{shop['handle']} 樸實手作的紋理裡藏著對生活的敬意，懂的人一定會珍惜。祝福今天出爐順利平安！✨"

def process_neighbor_walk(sample_size: int = 4, dry_run: bool = False) -> Dict[str, Any]:
    """執行友店巡邏與好友帳本沉澱"""
    ensure_data_dir()
    
    with open(FRIENDS_FILE, "r", encoding="utf-8") as f:
        friends_db = json.load(f)
        
    selected_shops = random.sample(SAMPLE_LOCAL_SHOPS, min(sample_size, len(SAMPLE_LOCAL_SHOPS)))
    actions = []
    
    for idx, shop in enumerate(selected_shops):
        handle = shop["handle"]
        is_deep_comment = (idx == 0) # 25% 留下深度讚美，其餘點讚留痕
        
        record = friends_db["interactions"].get(handle, {
            "name": shop["name"],
            "category": shop["category"],
            "visits_count": 0,
            "relationship_tier": "LEVEL_1_NEIGHBOR",
            "last_visited": None
        })
        
        record["visits_count"] += 1
        record["last_visited"] = datetime.now().isoformat()
        
        # 關係升階
        if record["visits_count"] >= 5:
            record["relationship_tier"] = "LEVEL_3_FAMILIAR_PARTNER"
        elif record["visits_count"] >= 2:
            record["relationship_tier"] = "LEVEL_2_WARM_FRIEND"
            
        friends_db["interactions"][handle] = record
        
        action_item = {
            "handle": handle,
            "name": shop["name"],
            "liked": True,
            "deep_comment": generate_artisan_praise(shop) if is_deep_comment else None,
            "new_tier": record["relationship_tier"],
            "visits_count": record["visits_count"]
        }
        actions.append(action_item)
        
    if not dry_run:
        friends_db["last_updated"] = datetime.now().isoformat()
        with open(FRIENDS_FILE, "w", encoding="utf-8") as f:
            json.dump(friends_db, f, ensure_ascii=False, indent=2)

    return {
        "status": "success",
        "atom": "atom-threads-neighbor-crm",
        "mode": "DRY_RUN" if dry_run else "PRODUCTION",
        "shops_visited_count": len(actions),
        "actions": actions,
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-neighbor-crm 在地友店聯盟與登門回禮原子")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬巡邏")
    parser.add_argument("--count", type=int, default=3, help="巡邏友店數量")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = process_neighbor_walk(sample_size=args.count, dry_run=args.dry_run)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"友店巡邏完成，共拜訪 {result['shops_visited_count']} 家在地好店。")

    sys.exit(0)

if __name__ == "__main__":
    main()
