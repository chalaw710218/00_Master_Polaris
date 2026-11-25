#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kage_real_learning.py - 影之真實數據學習引擎
讀取 threads-growth-auditor 累積的真實 Threads 快照 (insights_history.jsonl)，
以真實瀏覽/互動數據計算「鉤子」與「發文時段」的突觸權重，並寫入可重算的狀態檔。
不含任何預寫結論：所有數字皆由歷史檔即時計算；樣本不足時明確標示低信心。
"""

import sys
import os
import json
import argparse
import statistics
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_HISTORY = os.path.normpath(os.path.join(
    HERE, "..", "..", "threads-growth-auditor", "data", "insights_history.jsonl"))
STATE_PATH = os.path.normpath(os.path.join(HERE, "..", "vaults", "kage_synaptic_state.json"))
MIN_CONFIDENT_N = 3
HOOK_LEN = 3


def load_latest_posts(path: str):
    """逐行讀取快照；同一貼文 id 只保留最新快照的數據。"""
    posts, snapshots = {}, 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            snap = json.loads(line)
            snapshots += 1
            for p in snap.get("posts", []):
                p = dict(p)
                p["captured_at"] = snap.get("captured_at", "")
                prev = posts.get(p["id"])
                if prev is None or p["captured_at"] >= prev["captured_at"]:
                    posts[p["id"]] = p
    return list(posts.values()), snapshots


def delta_verifier(p: dict) -> float:
    """沿用原突觸方程之驗證誤差：互動率與瀏覽量（無後台轉粉數據時不計轉化項）。"""
    views = p.get("views", 0)
    replies = p.get("replies", 0)
    engagement = (replies / views) if views > 0 else 0.0
    return engagement * 10.0 + min(views, 500) / 500.0


def group_stats(posts, key_fn):
    groups = {}
    for p in posts:
        groups.setdefault(key_fn(p), []).append(p)
    out = {}
    for k, ps in groups.items():
        out[k] = {
            "n": len(ps),
            "avg_views": round(statistics.mean(x["views"] for x in ps), 1),
            "avg_er": round(statistics.mean(x.get("er", 0.0) for x in ps), 2),
            "weight": round(statistics.mean(delta_verifier(x) for x in ps), 4),
            "confidence": "OK" if len(ps) >= MIN_CONFIDENT_N else "LOW(樣本<%d)" % MIN_CONFIDENT_N,
        }
    return out


def learn(history_path: str):
    posts, snapshots = load_latest_posts(history_path)
    if not posts:
        return {"status": "NO_DATA", "history": history_path}

    hooks = group_stats(posts, lambda p: p["title"][:HOOK_LEN])
    hours = group_stats(posts, lambda p: "%02d時" % p["hour"])

    median_er = statistics.median(p.get("er", 0.0) for p in posts)
    # 溶酶體觀察名單：樣本足夠且平均互動率低於全帳號中位數
    watchlist = [
        {"hook": k, **v} for k, v in hooks.items()
        if v["n"] >= MIN_CONFIDENT_N and v["avg_er"] < median_er
    ]
    # 強化名單：樣本足夠且平均互動率不低於中位數
    reinforced = sorted(
        [{"hook": k, **v} for k, v in hooks.items()
         if v["n"] >= MIN_CONFIDENT_N and v["avg_er"] >= median_er],
        key=lambda x: x["weight"], reverse=True)

    best_hours = sorted(
        [{"hour": k, **v} for k, v in hours.items()],
        key=lambda x: x["avg_er"], reverse=True)[:3]

    state = {
        "learned_at": datetime.now().isoformat(),
        "source": history_path,
        "snapshots_read": snapshots,
        "unique_posts": len(posts),
        "account_median_er": median_er,
        "hook_weights": hooks,
        "hour_weights": hours,
    }
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    return {
        "status": "LEARNED_FROM_REAL_DATA",
        "snapshots_read": snapshots,
        "unique_posts": len(posts),
        "account_median_er": median_er,
        "reinforced_hooks": reinforced,
        "autophagy_watchlist": watchlist,
        "top_hours_by_er": best_hours,
        "caveat": "樣本量小，結論僅供假說；請以後續快照累積後再重算（本腳本每次重算、不會重複累加）。",
        "state_file": STATE_PATH,
    }


def main():
    ap = argparse.ArgumentParser(description="影之真實數據學習引擎")
    ap.add_argument("--learn", action="store_true", help="讀取真實快照並更新突觸權重")
    ap.add_argument("--history", default=DEFAULT_HISTORY, help="insights_history.jsonl 路徑")
    args = ap.parse_args()
    if not os.path.exists(args.history):
        print(json.dumps({"error": "找不到歷史檔", "path": args.history}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(learn(args.history), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
