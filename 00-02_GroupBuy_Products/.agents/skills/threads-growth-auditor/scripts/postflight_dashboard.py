"""第二軌：發布後客觀實證儀表板 (Post-Flight Empirical Audit)

自動由 Meta Threads API 探索最近貼文（不需手動維護 ID 清單），
計算互動率與破圈標籤，並將快照追加至 data/insights_history.jsonl。

用法：
  python postflight_dashboard.py [--limit 15] [--no-save]
"""
import argparse
import json
from datetime import datetime, timezone, timedelta

import requests

from _common import API_BASE, DATA_DIR, load_env

TPE = timezone(timedelta(hours=8))
BREAKOUT_VIEWS = 100  # 破 100 瀏覽 = 突破追蹤者圈層


def get_json(url, params):
    r = requests.get(url, params=params, timeout=30)
    return r.json()


def post_metrics(pid, token):
    res = get_json(f"{API_BASE}/{pid}/insights",
                   {"metric": "views,likes,replies,reposts,quotes", "access_token": token})
    m = {}
    for item in res.get("data", []):
        vals = item.get("values") or [{}]
        m[item.get("name")] = vals[0].get("value", 0)
    return m


def account_metrics(token):
    res = get_json(f"{API_BASE}/me/threads_insights",
                   {"metric": "views,followers_count", "access_token": token})
    out = {"followers": 0, "profile_views": 0}
    for item in res.get("data", []):
        if item.get("name") == "followers_count":
            out["followers"] = item.get("total_value", {}).get("value", 0)
        elif item.get("name") == "views":
            vals = item.get("values", [])
            if vals:
                out["profile_views"] = vals[-1].get("value", 0)
    return out


def tier(views, er):
    if views >= 250:
        return "🏆 爆款"
    if views >= BREAKOUT_VIEWS:
        return "🚀 破圈"
    if er >= 5:
        return "💬 高互動"
    return "🌱 累積中"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--no-save", action="store_true")
    a = ap.parse_args()

    env = load_env()
    token, uid = env.get("THREADS_ACCESS_TOKEN"), env.get("THREADS_USER_ID")
    if not token or not uid:
        raise SystemExit("❌ 缺少 THREADS_ACCESS_TOKEN / THREADS_USER_ID（.secrets.env）")

    acc = account_metrics(token)
    print(f"👥 追蹤者 {acc['followers']} 人｜👀 今日個人檔案瀏覽 {acc['profile_views']} 次\n")

    posts = get_json(f"{API_BASE}/{uid}/threads",
                     {"fields": "id,text,timestamp,permalink", "limit": a.limit,
                      "access_token": token}).get("data", [])

    rows, now = [], datetime.now(TPE).isoformat(timespec="seconds")
    for p in posts:
        m = post_metrics(p["id"], token)
        views = m.get("views", 0)
        inter = sum(m.get(k, 0) for k in ("likes", "replies", "reposts", "quotes"))
        er = (inter / views * 100) if views else 0.0
        ts = datetime.strptime(p["timestamp"], "%Y-%m-%dT%H:%M:%S%z").astimezone(TPE)
        age_h = (datetime.now(TPE) - ts).total_seconds() / 3600
        title = (p.get("text") or "").strip().split("\n")[0][:22]
        rows.append({"id": p["id"], "title": title, "hour": ts.hour, "age_h": round(age_h, 1),
                     "permalink": p.get("permalink"), "views": views,
                     "likes": m.get("likes", 0), "replies": m.get("replies", 0),
                     "reposts": m.get("reposts", 0), "quotes": m.get("quotes", 0),
                     "er": round(er, 1), "tier": tier(views, er)})

    rows.sort(key=lambda r: r["views"], reverse=True)
    print("| 貼文 | 發布時 | 瀏覽 | 讚 | 留言 | 轉發 | 互動率 | 評級 |")
    print("|---|---|--:|--:|--:|--:|--:|---|")
    for r in rows:
        note = " ⏳<24h" if r["age_h"] < 24 else ""
        print(f"| {r['title']} | {r['hour']:02d}時 | {r['views']} | {r['likes']} | "
              f"{r['replies']} | {r['reposts']} | {r['er']}% | {r['tier']}{note} |")

    # 時段診斷（僅採計已滿 24h 的貼文，避免未成熟數據誤導）
    mature = [r for r in rows if r["age_h"] >= 24]
    if mature:
        buckets = {}
        for r in mature:
            b = "清晨06-09" if 6 <= r["hour"] < 9 else "上午09-12" if 9 <= r["hour"] < 12 else \
                "午後12-18" if 12 <= r["hour"] < 18 else "晚間18-24" if r["hour"] >= 18 else "深夜00-06"
            buckets.setdefault(b, []).append(r["views"])
        print("\n⏱️ 時段平均瀏覽（僅滿 24h 貼文）：")
        for b, v in sorted(buckets.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
            print(f"  {b}：平均 {sum(v) / len(v):.0f} 次（n={len(v)}）")
        if len(mature) < 8:
            print("  ⚠️ 樣本數偏少（n<8），時段結論僅供參考，勿過度解讀。")

    if not a.no_save:
        DATA_DIR.mkdir(exist_ok=True)
        with open(DATA_DIR / "insights_history.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"captured_at": now, "account": acc, "posts": rows},
                               ensure_ascii=False) + "\n")
        print(f"\n💾 快照已追加至 data/insights_history.jsonl（{now}）")


if __name__ == "__main__":
    main()
