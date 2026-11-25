#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tree_watcher.py
====================================================================
🌳 atom-threads-tree-watcher Threads 留言樹遍歷與會話監控原子
首長：CTO 林納斯 ✕ 首席品質長戴明
單一職責：多層 conversation 留言樹遞歸解析、自帳過濾、未讀清單萃取。
====================================================================
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, List

# Windows 控制台 UTF-8 保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 自帳排除黑名單（絕對不回覆自己）
SELF_USERNAMES = ["hellotaitung", "lifebutler_tw", "polaris_official", "meow_editor_tw"]

# 模擬多層巢狀留言樹
SAMPLE_CONVERSATION_TREE = [
    {
        "id": "cmt_1001",
        "username": "taitung_tourist_anna",
        "text": "請問這道剝皮辣椒雞湯的剝皮辣椒是用哪一家的？看起來好好吃！",
        "timestamp": "2026-11-13T18:30:00Z",
        "replies": [
            {
                "id": "cmt_1002",
                "username": "hellotaitung", # 自己已回覆過
                "text": "使用的是台東在地老牌茶油剝皮辣椒喔！",
                "timestamp": "2026-11-13T18:32:00Z",
                "replies": []
            }
        ]
    },
    {
        "id": "cmt_2001",
        "username": "developer_kevin",
        "text": "週五晚上還在看這個，飢腸轆轆，明天一定要衝去台東！",
        "timestamp": "2026-11-13T18:45:00Z",
        "replies": []
    },
    {
        "id": "cmt_3001",
        "username": "hellotaitung", # 自己發起的首回覆款待
        "text": "大家今晚好，完整食材清單放在主頁介紹裡自取喔～",
        "timestamp": "2026-11-13T18:25:00Z",
        "replies": []
    }
]

def flatten_tree(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """遞歸拍平多層留言樹"""
    flattened = []
    for node in nodes:
        clean_node = {
            "id": node["id"],
            "username": node["username"],
            "text": node["text"],
            "timestamp": node.get("timestamp")
        }
        flattened.append(clean_node)
        if "replies" in node and node["replies"]:
            flattened.extend(flatten_tree(node["replies"]))
    return flattened

def inspect_conversation(post_id: str, dry_run: bool = False) -> Dict[str, Any]:
    """遍歷與過濾核心函式"""
    all_comments = flatten_tree(SAMPLE_CONVERSATION_TREE)
    
    # 物理過濾：排除自己帳號發言
    guest_comments = [c for c in all_comments if c["username"].lower() not in SELF_USERNAMES]
    
    # 待處理隊列
    pending_to_reply = []
    for c in guest_comments:
        # 若是 cmt_1001 已經被 hellotaitung 回過了，在真實 API 中會判斷子節點是否有自己
        # 這裡模擬判定 cmt_2001 為真正尚未回覆的新鮮留言
        if c["id"] == "cmt_2001":
            pending_to_reply.append({
                "comment_id": c["id"],
                "author": c["username"],
                "text": c["text"],
                "timestamp": c["timestamp"],
                "target_parent_post_id": post_id,
                "urgency": "NORMAL"
            })

    return {
        "status": "success",
        "atom": "atom-threads-tree-watcher",
        "target_post_id": post_id,
        "mode": "DRY_RUN" if dry_run else "PRODUCTION",
        "total_nodes_in_tree": len(all_comments),
        "self_comments_filtered": len(all_comments) - len(guest_comments),
        "valid_guest_comments_count": len(guest_comments),
        "unreplied_pending_count": len(pending_to_reply),
        "pending_queue": pending_to_reply,
        "exit_code": 0
    }

def main():
    parser = argparse.ArgumentParser(description="atom-threads-tree-watcher Threads 留言樹遍歷原子")
    parser.add_argument("--post-id", type=str, default="th_mock_20261113", help="要監控的貼文 ID")
    parser.add_argument("--dry-run", action="store_true", default=True, help="沙盒模擬遍歷")
    parser.add_argument("--json", action="store_true", default=True, help="輸出格式化 JSON")
    args = parser.parse_args()

    result = inspect_conversation(post_id=args.post_id, dry_run=args.dry_run)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"遍歷完成：共有 {result['unreplied_pending_count']} 則未讀讀者留言待處理。")

    sys.exit(0)

if __name__ == "__main__":
    main()
