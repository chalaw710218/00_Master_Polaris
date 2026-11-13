#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
taylor_real_learning.py - 泰勒絲之真實成效行銷學習引擎
讀取 threads-growth-auditor 累積的真實 Threads 快照，從標題抽取「行銷特徵」
（好奇提問句、闆仔互動梗、喵編人設、深夜時間詞、天氣題材、Emoji），
比較「有該特徵 vs 無該特徵」的真實瀏覽與互動差異。
所有數字皆即時計算；兩組任一組樣本 < 3 標示低信心，不下定論。
僅能從標題判斷特徵（歷史檔未存全文），此為已知限制。
"""

import sys
import os
import re
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
STATE_PATH = os.path.normpath(os.path.join(HERE, "..", "vaults", "taylor_marketing_state.json"))
MIN_N = 3

EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")

FEATURES = {
    "好奇提問句": lambda t: ("?" in t or "？" in t or t.startswith(("誰", "我就問", "你怎麼"))),
    "闆仔互動梗": lambda t: "闆仔" in t,
    "喵編人設": lambda t: "喵" in t,
    "深夜時間詞": lambda t: any(w in t for w in ("凌晨", "半夜", "十二點", "兩點", "一點")),
    "天氣題材": lambda t: any(w in t for w in ("氣象", "陸警", "風", "雨", "太陽", "颱")),
    "含Emoji": lambda t: bool(EMOJI_RE.search(t)),
}


def load_latest_posts(path):
    posts, snaps = {}, 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            snap = json.loads(line)
            snaps += 1
            for p in snap.get("posts", []):
                p = dict(p)
                p["captured_at"] = snap.get("captured_at", "")
                prev = posts.get(p["id"])
                if prev is None or p["captured_at"] >= prev["captured_at"]:
                    posts[p["id"]] = p
    return list(posts.values()), snaps


def summarize(ps):
    if not ps:
        return {"n": 0, "avg_views": None, "avg_er": None, "spread_rate_pct": None}
    views = sum(p["views"] for p in ps)
    spread = sum(p.get("reposts", 0) + p.get("quotes", 0) for p in ps)
    return {
        "n": len(ps),
        "avg_views": round(statistics.mean(p["views"] for p in ps), 1),
        "avg_er": round(statistics.mean(p.get("er", 0.0) for p in ps), 2),
        "spread_rate_pct": round(spread / views * 100, 2) if views else 0.0,
    }


def learn(path):
    posts, snaps = load_latest_posts(path)
    if not posts:
        return {"status": "NO_DATA", "history": path}

    results = {}
    for name, fn in FEATURES.items():
        with_f = [p for p in posts if fn(p["title"])]
        without_f = [p for p in posts if not fn(p["title"])]
        a, b = summarize(with_f), summarize(without_f)
        confident = a["n"] >= MIN_N and b["n"] >= MIN_N
        lift = None
        if confident and b["avg_er"]:
            lift = round(a["avg_er"] / b["avg_er"], 2)
        results[name] = {
            "有此特徵": a,
            "無此特徵": b,
            "互動率倍數(有/無)": lift,
            "信心": "OK" if confident else "LOW(任一組樣本<%d)" % MIN_N,
        }

    state = {
        "learned_at": datetime.now().isoformat(),
        "source": path,
        "snapshots_read": snaps,
        "unique_posts": len(posts),
        "feature_results": results,
    }
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    confident_hits = sorted(
        [(k, v["互動率倍數(有/無)"]) for k, v in results.items() if v["信心"] == "OK"],
        key=lambda x: x[1], reverse=True)

    return {
        "status": "LEARNED_FROM_REAL_DATA",
        "snapshots_read": snaps,
        "unique_posts": len(posts),
        "feature_results": results,
        "confident_ranking": [{"feature": k, "er_lift": v} for k, v in confident_hits],
        "caveat": "僅依標題判斷特徵、樣本小；結論為待驗證假說，不得直接當成行銷定律。",
        "state_file": STATE_PATH,
    }


def main():
    ap = argparse.ArgumentParser(description="泰勒絲之真實成效行銷學習引擎")
    ap.add_argument("--learn", action="store_true")
    ap.add_argument("--history", default=DEFAULT_HISTORY)
    args = ap.parse_args()
    if not os.path.exists(args.history):
        print(json.dumps({"error": "找不到歷史檔", "path": args.history}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(learn(args.history), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
