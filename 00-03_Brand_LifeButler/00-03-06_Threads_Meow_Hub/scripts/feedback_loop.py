#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feedback_loop.py — 生活管家脆（Threads）常態反饋測試與真對話審計閉環引擎

架構設計（依創辦人品碩親定之常態測試規範）：
1. log_post(post_id, k_ids, content)：記錄每次發文所綁定之儲備知識（["K-XXX"]）或對照組（[]）。
2. fetch_threads(post_id)：封裝 Meta Threads API 抓取 insights 與 replies，回傳 (指標字典, 回覆清單)。
3. collect(fetcher=fetch_threads)：每日收集後台物理真值，以「真對話回覆」（他人留言、長度>=10字，排除自身回覆）為核心判斷指標。
4. evaluate(report_path="feedback_report.md")：每週一評估實驗組與對照組差異，產出 feedback_report.md。
5. 晉升公理守則：一律等待創辦人（品碩）親自回「收」方可晉升。
"""

import os
import sys
import json
import time
import datetime
from pathlib import Path
import requests

# 確保 Windows PowerShell UTF-8 輸出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
HUB_DIR = SCRIPT_DIR.parent
DATA_DIR = HUB_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = DATA_DIR / "feedback_posts.json"
REPORT_FILE = HUB_DIR / "feedback_report.md"

ROOT_DIR = HUB_DIR.parents[1]
ENV_PATH = ROOT_DIR / ".secrets.env"


def load_env(env_path):
    if not env_path.exists():
        return {}
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()
    return env_vars


ENV = load_env(ENV_PATH)
TOKEN = ENV.get("THREADS_ACCESS_TOKEN")
USER_ID = ENV.get("THREADS_USER_ID")
API_BASE = "https://graph.threads.net/v1.0"
SELF_USERNAME = "hellotaitung"


def _read_log() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    try:
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _write_log(data: list[dict]):
    LOG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def get_all_k_ids() -> list[str]:
    """自 pending_knowledge_base.md 提取所有法定 K-編號"""
    kb_path = DATA_DIR / "pending_knowledge_base.md"
    if not kb_path.exists():
        return [f"K-{i:03d}" for i in range(1, 31)]
    text = kb_path.read_text(encoding="utf-8")
    import re
    k_ids = re.findall(r"###\s*【(K-\d+)・", text)
    return k_ids or [f"K-{i:03d}" for i in range(1, 31)]


def select_next_k_id(preferred_k_id: str = None) -> list[str]:
    """
    依創辦人品碩指示挑選儲備知識：
    1. 每次發文只選 1 條來寫（回傳 ["K-XXX"]）。
    2. 每天保留 1 篇不用任何知識，當對照組（回傳 []）。
    3. 若手動指定 preferred_k_id：
       - 若為 'control'、'[]'、'none'，回傳 []。
       - 否則標準化後回傳 [preferred_k_id]。
    4. 若無指定：
       - 檢查今日是否已存在對照組 []，若無則回傳 [] 作為當日對照組。
       - 若今日已發布對照組，則自儲備知識庫中挑選測試次數最少者（覆蓋平衡），回傳 [chosen_k_id]。
    """
    if preferred_k_id:
        pid = str(preferred_k_id).strip()
        if pid.lower() in ("control", "none", "[]", ""):
            return []
        if not pid.upper().startswith("K-") and pid.isdigit():
            pid = f"K-{int(pid):03d}"
        else:
            pid = pid.upper()
        return [pid]

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    posts = _read_log()
    today_posts = [p for p in posts if str(p.get("created_at", "")).startswith(today_str)]
    has_today_control = any(len(p.get("k_ids", [])) == 0 or p.get("is_control") for p in today_posts)

    if not has_today_control:
        return []

    all_k = get_all_k_ids()
    counts = {k: 0 for k in all_k}
    for p in posts:
        for k in p.get("k_ids", []):
            if k in counts:
                counts[k] += 1

    sorted_k = sorted(all_k, key=lambda k: counts[k])
    chosen = sorted_k[0] if sorted_k else "K-001"
    return [chosen]


def log_post(post_id: str, k_ids: list[str], content: str) -> dict:
    """
    發文成功後呼叫：
    post_id: Threads 官方貼文 ID
    k_ids: 儲備知識編號清單（如 ["K-014"]），若為當日對照組則傳入 []
    content: 發布之內文
    """
    posts = _read_log()
    now_str = datetime.datetime.now().isoformat(timespec="seconds")

    # 去重或更新
    for p in posts:
        if p.get("post_id") == post_id:
            p["k_ids"] = k_ids
            p["content"] = content
            p["updated_at"] = now_str
            _write_log(posts)
            print(f"📝 [feedback_loop] 已更新貼文紀錄: {post_id} (K-IDs: {k_ids})")
            return p

    entry = {
        "post_id": str(post_id),
        "k_ids": k_ids or [],
        "is_control": (len(k_ids or []) == 0),
        "content": content,
        "created_at": now_str,
        "metrics": {},
        "replies": [],
        "true_dialogue_replies": [],
        "true_dialogue_count": 0,
        "last_collected_at": None,
        "evaluated": False,
    }
    posts.append(entry)
    _write_log(posts)
    group_label = "對照組 []" if entry["is_control"] else f"實驗組 {k_ids}"
    print(f"📝 [feedback_loop] 成功登記新貼文: {post_id} | {group_label}")
    return entry


def fetch_threads(post_id: str) -> tuple[dict, list[dict]]:
    """
    調用 Meta Threads Graph API 抓取 insights 與 replies
    回傳：(指標字典, 回覆清單)
    """
    if not TOKEN or not post_id:
        return {}, []

    # 1. 抓取 Insights 指標
    metrics = {"views": 0, "likes": 0, "replies": 0, "reposts": 0, "quotes": 0}
    insights_url = f"{API_BASE}/{post_id}/insights?metric=views,likes,replies,reposts,quotes&access_token={TOKEN}"
    try:
        r = requests.get(insights_url, timeout=15)
        if r.status_code == 200:
            for item in r.json().get("data", []):
                val = item.get("values", [{}])[0].get("value", 0)
                metrics[item.get("name")] = val
    except Exception as e:
        print(f"⚠️ [feedback_loop] 讀取 Insights 警告 ({post_id}): {e}")

    # 2. 抓取 Replies 回覆清單
    replies_list = []
    replies_url = f"{API_BASE}/{post_id}/replies?fields=id,text,timestamp,username&access_token={TOKEN}"
    try:
        r = requests.get(replies_url, timeout=15)
        if r.status_code == 200:
            for item in r.json().get("data", []):
                uname = item.get("username", "")
                text = item.get("text", "")
                is_self = (uname.lower() == SELF_USERNAME.lower()) or (uname == "")
                replies_list.append({
                    "id": item.get("id"),
                    "text": text,
                    "username": uname,
                    "is_self": is_self,
                    "timestamp": item.get("timestamp"),
                })
    except Exception as e:
        print(f"⚠️ [feedback_loop] 讀取 Replies 警告 ({post_id}): {e}")

    return metrics, replies_list


def collect(fetcher=fetch_threads) -> dict:
    """
    每天跑 collect：遍歷已登記貼文，調用 fetcher 取得最新物理數據，
    並依「他人留言且>=10字（不含自身）」精算真對話回覆數。
    """
    posts = _read_log()
    if not posts:
        print("ℹ️ [feedback_loop] 目前尚無已登記之貼文記錄，無須收集。")
        return {"total_collected": 0}

    print(f"📡 [feedback_loop] 開始執行每日數據收集 (總登記貼文: {len(posts)} 篇)...")
    collected_count = 0
    now_str = datetime.datetime.now().isoformat(timespec="seconds")

    for p in posts:
        pid = p["post_id"]
        try:
            metrics, replies = fetcher(pid)
        except Exception as e:
            print(f"❌ 抓取失敗 ({pid}): {e}")
            continue

        p["metrics"] = metrics
        p["replies"] = replies

        # 核心標準：別人留的、10字以上、不算自己
        true_dialogues = []
        for r in replies:
            text = str(r.get("text", "")).strip()
            is_self = r.get("is_self", False)
            if not is_self and len(text) >= 10:
                true_dialogues.append({
                    "username": r.get("username"),
                    "text": text,
                    "timestamp": r.get("timestamp"),
                })

        p["true_dialogue_replies"] = true_dialogues
        p["true_dialogue_count"] = len(true_dialogues)
        p["last_collected_at"] = now_str
        collected_count += 1
        print(f"   ✅ Post {pid} 收集完成: Views={metrics.get('views', 0)} | 真對話回覆={len(true_dialogues)} 則")

    _write_log(posts)
    print(f"✨ [feedback_loop] 本輪數據收集完成，共更新 {collected_count} 篇貼文。")
    return {"total_collected": collected_count}


def evaluate(report_path=REPORT_FILE) -> str:
    """
    每週一跑 evaluate：
    比對實驗組 (各 K-編號) vs 對照組 ([]) 之「真對話回覆」成效，
    生成 feedback_report.md。
    """
    posts = _read_log()
    rp = Path(report_path)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not posts:
        md = f"# 📊 Threads 常態反饋測試與真對話審計週報\n\n- **產出時間**：{now_str}\n- **狀態**：尚未登記任何發文測試數據。\n"
        rp.write_text(md, encoding="utf-8")
        return md

    # 分組統計
    k_stats: dict[str, dict] = {}
    control_stats = {"count": 0, "total_views": 0, "total_true_replies": 0, "posts": []}

    for p in posts:
        k_ids = p.get("k_ids", [])
        views = p.get("metrics", {}).get("views", 0)
        td_count = p.get("true_dialogue_count", 0)

        if not k_ids or p.get("is_control"):
            control_stats["count"] += 1
            control_stats["total_views"] += views
            control_stats["total_true_replies"] += td_count
            control_stats["posts"].append(p)
        else:
            for kid in k_ids:
                if kid not in k_stats:
                    k_stats[kid] = {"count": 0, "total_views": 0, "total_true_replies": 0, "posts": []}
                k_stats[kid]["count"] += 1
                k_stats[kid]["total_views"] += views
                k_stats[kid]["total_true_replies"] += td_count
                k_stats[kid]["posts"].append(p)

    ctrl_avg_td = (control_stats["total_true_replies"] / control_stats["count"]) if control_stats["count"] > 0 else 0.0
    ctrl_avg_views = (control_stats["total_views"] / control_stats["count"]) if control_stats["count"] > 0 else 0.0

    lines = [
        "# 📊 Threads 常態反饋測試與真對話審計週報 (Feedback Report)",
        "",
        f"- **統計基準時間**：{now_str}",
        f"- **追蹤貼文總數**：{len(posts)} 篇（對照組：{control_stats['count']} 篇，實驗組：{len(posts) - control_stats['count']} 篇）",
        f"- **唯一評判硬標準**：**「真對話回覆」**（排除管家自身回覆、真實網友留言、字數 >= 10 字）",
        f"- **公理晉級守則**：**一律等待創辦人（品碩）親自回「收」解鎖晉升**",
        "",
        "---",
        "",
        "## 一、 對照組基準線 (Control Group: `[]`)",
        f"- **樣本數**：{control_stats['count']} 篇",
        f"- **平均瀏覽數 (Views)**：{ctrl_avg_views:.1f}",
        f"- **平均真對話回覆數**：**{ctrl_avg_td:.2f} 則／篇**",
        "",
        "---",
        "",
        "## 二、 各儲備知識實驗組成效榜 (K-IDs vs Control)",
        "| 儲備知識編號 | 測試篇數 | 平均真對話回覆 | 平均 Views | 對比對照組倍率 | 實戰狀態判定 |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    candidates_for_axiom = []

    for kid, s in sorted(k_stats.items()):
        c = s["count"]
        avg_td = s["total_true_replies"] / c if c > 0 else 0.0
        avg_v = s["total_views"] / c if c > 0 else 0.0
        ratio_str = f"{(avg_td / ctrl_avg_td):.2f}x" if ctrl_avg_td > 0 else "基準為0"

        if avg_td > ctrl_avg_td and c >= 2:
            status = "🌟 具備公理晉級潛力 (待品碩確認)"
            candidates_for_axiom.append((kid, avg_td, c))
        elif avg_td >= ctrl_avg_td:
            status = "🟡 樣本積累中 (持平)"
        else:
            status = "🔻 低於對照組 (待修正)"

        lines.append(f"| **{kid}** | {c} | **{avg_td:.2f} 則** | {avg_v:.1f} | {ratio_str} | {status} |")

    if not k_stats:
        lines.append("| *(暫無實驗組數據)* | 0 | 0.0 則 | 0.0 | - | 待發布新貼文 |")

    lines.extend([
        "",
        "---",
        "",
        "## 三、 具備公理晉級潛力清單（待創辦人審批）",
    ])

    if candidates_for_axiom:
        for kid, avg_td, c in candidates_for_axiom:
            lines.append(f"- **{kid}**：實測 {c} 篇，平均帶來 **{avg_td:.2f} 則真對話**，明顯高於對照組。")
            lines.append(f"  * 🔒 **狀態**：等待創辦人（品碩）回覆「收」即刻晉升入公理庫！")
    else:
        lines.append("- 目前尚無滿足連續正向且顯著勝出之儲備知識，持續保持常態測試，杜絕盲目升級。")

    lines.extend([
        "",
        "---",
        "",
        "## 四、 近期真對話回覆原樣摘錄（他人留言且 >= 10 字）",
    ])

    has_real_reply = False
    for p in posts:
        tds = p.get("true_dialogue_replies", [])
        if tds:
            has_real_reply = True
            lines.append(f"### 📍 貼文 `{p['post_id']}` (組別: {p.get('k_ids') or '對照組'})")
            for r in tds:
                lines.append(f"- **@{r.get('username')}**：{r.get('text')}")
            lines.append("")

    if not has_real_reply:
        lines.append("- 尚無收集到 10 字以上之真實網友對話留言。")

    report_text = "\n".join(lines) + "\n"
    rp.write_text(report_text, encoding="utf-8")
    print(f"📑 [feedback_loop] 週報已成功生成: {rp.name}")
    return report_text


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Feedback Loop CLI")
    parser.add_argument("--collect", action="store_true", help="執行每日數據收集")
    parser.add_argument("--evaluate", action="store_true", help="執行每週評估並產出報告")
    parser.add_argument("--log-test", action="store_true", help="登記一筆測試貼文")
    args = parser.parse_args()

    if args.log_test:
        log_post("test_post_001", ["K-014"], "測試感官白描貼文")
    if args.collect:
        collect()
    if args.evaluate:
        text = evaluate()
        print(text)
    if not (args.collect or args.evaluate or args.log_test):
        parser.print_help()
