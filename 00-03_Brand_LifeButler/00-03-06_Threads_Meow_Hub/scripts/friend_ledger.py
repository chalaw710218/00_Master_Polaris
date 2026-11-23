#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
極星社群好友互動帳本 (Friend Relationship Ledger)
記錄與管理 Threads 友店互動歷史、拜訪次數與關係溫度階梯。
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "friend_interactions.json"
TARGETS_FILE = BASE_DIR / "scripts" / "following_targets.json"

def is_comment_or_reply(action: str) -> bool:
    """創辦人親定：「互動」只計算留言和回覆，不計算按讚與純造訪"""
    act = (action or "").lower()
    return ("comment" in act) or ("reply" in act)

def count_valid_interactions(friend_entry: dict) -> int:
    """從 history 精算有效互動次數（僅計留言與回覆）"""
    history = friend_entry.get("history", [])
    return sum(1 for h in history if is_comment_or_reply(h.get("action", "")))

def calculate_tier(comment_reply_count: int) -> str:
    if comment_reply_count >= 5:
        return "🤝 摯友同盟"
    elif comment_reply_count >= 2:
        return "☕ 熟稔常客"
    elif comment_reply_count >= 1:
        return "🌱 初次問候"
    else:
        return "👀 僅點讚/造訪"

def load_ledger():
    if not DATA_FILE.exists():
        return {"last_updated": datetime.now().isoformat(), "summary": {}, "friends": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"讀取好友帳本 {DATA_FILE} 失敗: {e}") from e

def save_ledger(data):
    data["last_updated"] = datetime.now().isoformat()
    # 重新計算每位好友的有效互動（僅計留言與回覆）與 summary
    for f in data.get("friends", {}).values():
        valid_cnt = count_valid_interactions(f)
        f["comments_given"] = valid_cnt
        f["relationship_tier"] = calculate_tier(valid_cnt)

    total_friends = len(data.get("friends", {}))
    total_comments = sum(f.get("comments_given", 0) for f in data.get("friends", {}).values())
    total_likes = sum(f.get("likes_given", 0) for f in data.get("friends", {}).values())
    data["summary"] = {
        "total_friends_contacted": total_friends,
        "total_interactions": total_comments,
        "total_likes": total_likes,
        "total_comments": total_comments
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def record_interaction(username, name, action="comment", post_url="", comment_text="", screenshot=""):
    data = load_ledger()
    friends = data.setdefault("friends", {})
    clean_user = username.replace("@", "").strip().lower()

    now_iso = datetime.now().isoformat()

    if clean_user not in friends:
        friends[clean_user] = {
            "username": clean_user,
            "name": name,
            "category": "local_community",
            "total_interactions": 0,
            "likes_given": 0,
            "comments_given": 0,
            "relationship_tier": "👀 僅點讚/造訪",
            "first_contact_at": now_iso,
            "last_interaction_at": now_iso,
            "history": []
        }

    f = friends[clean_user]
    if "like" in action:
        f["likes_given"] = f.get("likes_given", 0) + 1

    history_item = {
        "timestamp": now_iso,
        "action": action,
        "post_url": post_url,
        "comment_text": comment_text,
        "screenshot": screenshot
    }
    f["history"].append(history_item)
    valid_cnt = count_valid_interactions(f)
    f["comments_given"] = valid_cnt
    f["total_interactions"] = valid_cnt
    f["relationship_tier"] = calculate_tier(valid_cnt)
    f["last_interaction_at"] = now_iso

    save_ledger(data)
    print(f"✅ 成功記錄與 {name} (@{clean_user}) 的互動！當前有效留言/回覆互動: {valid_cnt} 次 | 關係階梯: {f['relationship_tier']}")
    return f

def print_dashboard():
    data = load_ledger()
    summary = data.get("summary", {})
    friends = data.get("friends", {})

    print("\n=================================================================")
    print(" 🗺️  極星社群好友互動帳本（Friend Relationship Ledger）")
    print("=================================================================")
    print(f" 累計拜訪好友數：{summary.get('total_friends_contacted', 0)} 位")
    print(f" 總互動次數：{summary.get('total_interactions', 0)} 次 (愛心: {summary.get('total_likes', 0)} | 留言: {summary.get('total_comments', 0)})")
    print(f" 最後更新時間：{data.get('last_updated', 'N/A')}")
    print("-----------------------------------------------------------------")
    print(f"{'好友/店名':<16} {'帳號':<18} {'次數':<6} {'階梯':<14} {'最後拜訪時間':<20}")
    print("-----------------------------------------------------------------")

    # 按互動次數降序排列
    sorted_friends = sorted(friends.values(), key=lambda x: x.get("total_interactions", 0), reverse=True)
    for f in sorted_friends:
        name = f.get("name", "")[:12]
        user = "@" + f.get("username", "")[:15]
        cnt = f.get("total_interactions", 0)
        tier = f.get("relationship_tier", "🌱 初次問候")
        last_t = f.get("last_interaction_at", "")[:16].replace("T", " ")
        print(f"{name:<16} {user:<18} {cnt:<6} {tier:<14} {last_t:<20}")

    print("=================================================================\n")

def recommend_next(top_n=3):
    """
    從 185 家追蹤庫中，智慧推薦下一次「去逛逛」應優先拜訪的好友名單
    規則：
    1. 尚未拜訪過的友店（次數 = 0）
    2. 或距離上次拜訪時間最久的友店
    """
    if not TARGETS_FILE.exists():
        print("未找到 following_targets.json")
        return []

    data = load_ledger()
    visited_map = data.get("friends", {})

    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        targets_data = json.load(f)

    all_targets = []
    for cat_name, items in targets_data.get("categories", {}).items():
        for item in items:
            uname = item.get("username", "").strip().lower()
            all_targets.append({
                "username": uname,
                "name": item.get("name", uname),
                "category": cat_name,
                "strategic_value": item.get("strategic_value", "")
            })

    # 分類候選名單
    candidates = []
    for t in all_targets:
        u = t["username"]
        if u in visited_map:
            t["interactions"] = visited_map[u].get("total_interactions", 0)
            t["last_visited"] = visited_map[u].get("last_interaction_at", "1970-01-01")
        else:
            t["interactions"] = 0
            t["last_visited"] = "1970-01-01"
        candidates.append(t)

    # 排序：互動次數最少者優先，次數相同則最後拜訪時間最早者優先
    sorted_candidates = sorted(candidates, key=lambda x: (x["interactions"], x["last_visited"]))
    top_picks = sorted_candidates[:top_n]

    print(f"\n💡 智慧漫遊建議：下次「去逛逛」建議優先拜訪的 {top_n} 位友店：")
    for idx, c in enumerate(top_picks, 1):
        print(f" {idx}. {c['name']} (@{c['username']}) - 累積互動: {c['interactions']} 次 | 價值: {c['strategic_value'][:28]}...")
    print()
    return top_picks

def main():
    parser = argparse.ArgumentParser(description="極星社群好友互動帳本")
    parser.add_argument("--list", action="store_true", help="列出所有好友互動紀錄與階梯")
    parser.add_argument("--recommend", type=int, default=0, help="智慧推薦下次應拜訪的好友數量 (例如 --recommend 3)")
    parser.add_argument("--record", action="store_true", help="手動新增一筆互動紀錄")
    parser.add_argument("--user", type=str, help="帳號 (username)")
    parser.add_argument("--name", type=str, help="好友/店名")
    parser.add_argument("--action", type=str, default="comment", help="動作類型 (like, comment, like_and_comment)")
    parser.add_argument("--text", type=str, default="", help="留言內容")
    parser.add_argument("--url", type=str, default="", help="貼文網址")
    parser.add_argument("--shot", type=str, default="", help="截圖路徑")
    args = parser.parse_args()

    if args.record:
        if not args.user or not args.name:
            print("Error: --user and --name are required when --record is specified.")
            sys.exit(1)
        record_interaction(args.user, args.name, args.action, args.url, args.text, args.shot)
    elif args.recommend > 0:
        recommend_next(args.recommend)
    else:
        print_dashboard()

if __name__ == "__main__":
    main()
