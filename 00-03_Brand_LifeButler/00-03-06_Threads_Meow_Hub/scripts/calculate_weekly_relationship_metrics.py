#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polaris Threads Weekly Relationship Metrics Calculator (每週四項在地關係科學指標統計程式)
作者: 影 (Shadow · 首席特務兼生活管家)

創辦人（品碩）親定四項週指標（100% 由程式從紀錄計算，不准手寫）：
(1) 走心留言數：從 data/daily_interaction_limits.json 的 history 計算。
(2) 得到對方回覆數：用通知頁 (threads.net/activity) 抓取「回覆了你的留言」通知存進紀錄檔；
    週報從紀錄檔計算，同一則留言被回多次只算 1。
(3) 回訪留言人數：用 API 抓本週我們自己貼文的 conversation，計算留言 10 字以上的不重複帳號數（排除自己）。
(4) 熟稔常客人數：從 friend_ledger (data/friend_interactions.json) 計算互動 2 次以上的帳號數。
"""

import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime, date, timedelta

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data"
SESSION_PATH = SCRIPT_DIR / "threads_session.json"

LIMITS_FILE = DATA_DIR / "daily_interaction_limits.json"
ACTIVITY_LOG_FILE = DATA_DIR / "activity_replies_log.json"
FRIEND_LEDGER_FILE = DATA_DIR / "friend_interactions.json"
WEEKLY_REPORT_FILE = DATA_DIR / "weekly_relationship_metrics.json"

sys.path.insert(0, str(SCRIPT_DIR))
try:
    from threads_publisher import THREADS_ACCESS_TOKEN, THREADS_USER_ID, API_BASE
except ImportError:
    THREADS_ACCESS_TOKEN = None
    THREADS_USER_ID = None
    API_BASE = "https://graph.threads.net/v1.0"

SELF_USERNAMES = {"hellotaitung"}


def get_week_start_date(custom_start: str = None) -> date:
    """預設取本週一 (Monday) 作為本週起始日"""
    if custom_start:
        return date.fromisoformat(custom_start)
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday


def parse_iso_date(ts_str: str) -> date | None:
    if not ts_str:
        return None
    try:
        clean = ts_str.replace("Z", "+00:00")
        if "+0000" in clean:
            clean = clean.replace("+0000", "+00:00")
        dt = datetime.fromisoformat(clean)
        return dt.date()
    except Exception:
        try:
            return date.fromisoformat(ts_str[:10])
        except Exception:
            return None


# =====================================================================
# (1) 走心留言數：從 daily_interaction_limits.json 的 history 計算
# =====================================================================
def calculate_metric_1_heartfelt_comments(week_start: date) -> tuple[int, list]:
    if not LIMITS_FILE.exists():
        return 0, []

    try:
        with open(LIMITS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return 0, []

    history = data.get("history", [])
    matched = []
    for item in history:
        if item.get("type") != "comment":
            continue
        post_url = item.get("post_url", "")
        if "/post/test" in post_url:
            continue
        item_date = parse_iso_date(item.get("timestamp", ""))
        if item_date and item_date >= week_start:
            text = (item.get("comment_text") or "").strip()
            if len(text) >= 10:
                matched.append(item)

    return len(matched), matched


# =====================================================================
# (2) 得到對方回覆數：從 threads.net/activity 抓取並寫入紀錄檔，同留言被回多次算 1
# =====================================================================
def load_activity_log() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if ACTIVITY_LOG_FILE.exists():
        try:
            with open(ACTIVITY_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_fetched": None, "replies": []}


def save_activity_log(log_data: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ACTIVITY_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def fetch_activity_replies_from_web(commented_records: list) -> int:
    """
    每天抓一次 threads.net/activity「回覆了你的留言」通知，存入 data/activity_replies_log.json
    """
    log_data = load_activity_log()
    existing_ids = {r.get("event_id") for r in log_data.get("replies", [])}
    commented_users = {c.get("target_user", "").lower() for c in commented_records if c.get("target_user")}
    commented_urls = {c.get("post_url", "") for c in commented_records if c.get("post_url")}

    if not SESSION_PATH.exists():
        print("   ⚠️ 未找到 threads_session.json，跳過網頁通知抓取，直接讀取本地紀錄檔。")
        return 0

    new_added = 0
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                storage_state=str(SESSION_PATH),
                viewport={"width": 1280, "height": 900},
                locale="zh-TW"
            )
            page = context.new_page()
            print("   🌐 正在巡檢 Threads 通知中心 (https://www.threads.net/activity)...", flush=True)
            page.goto("https://www.threads.net/activity", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(4500)

            # 擷取通知區塊中含有「回覆了你的留言」或來自我們已留言對象的回覆通知
            anchors = page.locator('a[href*="/post/"]').all()
            for a in anchors:
                try:
                    href = a.get_attribute("href") or ""
                    if "/post/" not in href:
                        continue
                    full_url = f"https://www.threads.net{href}" if href.startswith("/") else href
                    container_text = a.locator("xpath=ancestor::div[contains(@class, '')][position()<=4]").first.inner_text(timeout=1000)
                except Exception:
                    container_text = ""
                    full_url = ""

                if not container_text:
                    continue

                is_reply_to_comment = any(
                    kw in container_text
                    for kw in ["回覆了你的留言", "回覆了你的串文回覆", "replied to your reply", "replied to your comment"]
                )

                # 或該貼文網址命中我們主動去留言過的外部貼文
                matched_our_comment_url = None
                for c_url in commented_urls:
                    if c_url and c_url.split("/post/")[-1][:11] in full_url:
                        matched_our_comment_url = c_url
                        is_reply_to_comment = True
                        break

                if is_reply_to_comment:
                    # 同一則留言被回多次只算 1：以「我方原留言所屬之目標貼文/節點」作為唯一歸戶鍵 (our_comment_key)
                    comment_key = matched_our_comment_url or full_url
                    event_id = f"{comment_key}::{container_text[:40]}"
                    if event_id not in existing_ids:
                        log_data.setdefault("replies", []).append({
                            "event_id": event_id,
                            "fetched_at": datetime.now().isoformat(),
                            "date": date.today().isoformat(),
                            "our_comment_key": comment_key,
                            "post_url": full_url,
                            "raw_snippet": container_text[:120].replace("\n", " ")
                        })
                        existing_ids.add(event_id)
                        new_added += 1

            browser.close()
    except Exception as e:
        print(f"   ⚠️ 通知中心抓取提示: {e}")

    log_data["last_fetched"] = datetime.now().isoformat()
    save_activity_log(log_data)
    return new_added


def calculate_metric_2_replies_received(week_start: date, commented_records: list, skip_fetch: bool = False) -> tuple[int, list]:
    if not skip_fetch:
        fetch_activity_replies_from_web(commented_records)

    log_data = load_activity_log()
    replies = log_data.get("replies", [])

    # 同一則留言被回多次只算 1 -> 以 our_comment_key 去重
    unique_comment_keys = {}
    for r in replies:
        r_date = parse_iso_date(r.get("date") or r.get("fetched_at", ""))
        if r_date and r_date >= week_start:
            ckey = r.get("our_comment_key") or r.get("post_url")
            if ckey and ckey not in unique_comment_keys:
                unique_comment_keys[ckey] = r

    return len(unique_comment_keys), list(unique_comment_keys.values())


# =====================================================================
# (3) 回訪留言人數：用 API 抓本週我們自己貼文的 conversation，計算 >=10 字不重複帳號數
# =====================================================================
def calculate_metric_3_return_commenters(week_start: date) -> tuple[int, list]:
    if not THREADS_ACCESS_TOKEN or not THREADS_USER_ID:
        print("   ⚠️ 未載入 THREADS_ACCESS_TOKEN，無法呼叫 API 查詢 conversation。")
        return 0, []

    unique_users = {}
    try:
        t_url = (
            f"{API_BASE}/{THREADS_USER_ID}/threads"
            f"?fields=id,text,permalink,timestamp&limit=25&access_token={THREADS_ACCESS_TOKEN}"
        )
        res = requests.get(t_url, timeout=20).json()
        posts = res.get("data", [])

        for post in posts:
            pid = post.get("id")
            p_date = parse_iso_date(post.get("timestamp", ""))
            if not p_date or p_date < week_start:
                continue

            c_url = (
                f"{API_BASE}/{pid}/conversation"
                f"?fields=id,text,timestamp,username,permalink&access_token={THREADS_ACCESS_TOKEN}"
            )
            c_res = requests.get(c_url, timeout=15).json()
            comments = c_res.get("data", [])

            for c in comments:
                uname = (c.get("username") or "").strip().lower()
                text = (c.get("text") or "").strip()
                c_date = parse_iso_date(c.get("timestamp", ""))

                if not uname or uname in SELF_USERNAMES:
                    continue
                if c_date and c_date < week_start:
                    continue
                if len(text) >= 10:
                    if uname not in unique_users:
                        unique_users[uname] = {
                            "username": uname,
                            "text": text,
                            "post_id": pid,
                            "timestamp": c.get("timestamp")
                        }
    except Exception as e:
        print(f"   ⚠️ API 抓取自帳 conversation 異常: {e}")

    return len(unique_users), list(unique_users.values())


# =====================================================================
# (4) 熟稔常客人數：從 friend_ledger 計算互動 2 次以上的帳號數
#     規則：friend_ledger 不歸零；「互動」只計算留言和回覆，不計算按讚；
#     分開列兩個數字：累計熟客數、本週新增熟客數（本週才達到 2 次互動門檻的帳號）
# =====================================================================
def is_comment_or_reply_action(action: str) -> bool:
    act = (action or "").lower()
    return ("comment" in act) or ("reply" in act)


def calculate_metric_4_familiar_regulars(week_start: date) -> tuple[int, int, list, list]:
    if not FRIEND_LEDGER_FILE.exists():
        return 0, 0, [], []

    try:
        with open(FRIEND_LEDGER_FILE, "r", encoding="utf-8") as f:
            ledger = json.load(f)
    except Exception as e:
        raise RuntimeError(f"讀取 {FRIEND_LEDGER_FILE} 失敗: {e}") from e

    friends = ledger.get("friends", {})
    cumulative_regulars = []
    new_regulars_this_week = []

    for uname, info in friends.items():
        history = info.get("history", [])
        # 只計算留言與回覆，不計算按讚 (like) 與純造訪 (visit)
        valid_items = [h for h in history if is_comment_or_reply_action(h.get("action", ""))]
        total_valid = len(valid_items)

        if total_valid >= 2:
            before_week_valid = 0
            for h in valid_items:
                h_date = parse_iso_date(h.get("timestamp", ""))
                if not h_date or h_date < week_start:
                    before_week_valid += 1

            is_new_this_week = (before_week_valid < 2) and (total_valid >= 2)
            entry = {
                "username": uname,
                "name": info.get("name", uname),
                "comment_reply_interactions": total_valid,
                "before_week_interactions": before_week_valid,
                "is_new_this_week": is_new_this_week
            }
            cumulative_regulars.append(entry)
            if is_new_this_week:
                new_regulars_this_week.append(entry)

    cumulative_regulars.sort(key=lambda x: x["comment_reply_interactions"], reverse=True)
    new_regulars_this_week.sort(key=lambda x: x["comment_reply_interactions"], reverse=True)
    return len(cumulative_regulars), len(new_regulars_this_week), cumulative_regulars, new_regulars_this_week


def main():
    parser = argparse.ArgumentParser(description="計算每週四項台東在地關係指標")
    parser.add_argument("--start-date", type=str, default=None, help="指定週起始日 (YYYY-MM-DD)，預設為本週一")
    parser.add_argument("--skip-activity-fetch", action="store_true", help="跳過開啟瀏覽器抓通知頁，僅從現有紀錄檔計算")
    parser.add_argument("--fetch-activity-only", action="store_true", help="僅執行每日通知頁巡檢並累積寫入 activity_replies_log.json")
    args = parser.parse_args()

    week_start = get_week_start_date(args.start_date)
    today_str = date.today().isoformat()

    # (1) 走心留言數
    m1_count, m1_list = calculate_metric_1_heartfelt_comments(week_start)

    if args.fetch_activity_only:
        print(f"🌐 [每日通知頁自動巡檢] 正在抓取 threads.net/activity 並累積寫入 {ACTIVITY_LOG_FILE.name}...")
        added = fetch_activity_replies_from_web(m1_list)
        log_data = load_activity_log()
        print(f"✅ 巡檢完畢！本次新增 {added} 筆回覆通知，目前紀錄檔累計 {len(log_data.get('replies', []))} 筆。")
        return

    print("============================================================")
    print("📊 生活管家 Threads 每週在地關係四項指標統計 (程式自動精算)")
    print(f"📅 統計區間: {week_start.isoformat()} ~ {today_str}")
    print("============================================================")

    # (2) 得到對方回覆數
    m2_count, m2_list = calculate_metric_2_replies_received(
        week_start, m1_list, skip_fetch=args.skip_activity_fetch
    )

    # (3) 回訪留言人數
    m3_count, m3_list = calculate_metric_3_return_commenters(week_start)

    # (4) 熟稔常客人數 (僅計留言和回覆，不計按讚；分列累計與本週新增)
    m4_cumulative_count, m4_new_count, m4_cumulative_list, m4_new_list = calculate_metric_4_familiar_regulars(week_start)

    report = {
        "calculated_at": datetime.now().isoformat(),
        "week_start": week_start.isoformat(),
        "week_end": today_str,
        "metrics": {
            "1_heartfelt_comments_sent": m1_count,
            "2_replies_received_unique_comments": m2_count,
            "3_return_commenters_unique_users_10chars": m3_count,
            "4_familiar_regulars_cumulative": m4_cumulative_count,
            "4_familiar_regulars_new_this_week": m4_new_count
        },
        "details": {
            "heartfelt_comments": m1_list,
            "replies_received": m2_list,
            "return_commenters": m3_list,
            "familiar_regulars_cumulative": m4_cumulative_list,
            "familiar_regulars_new_this_week": m4_new_list
        }
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(WEEKLY_REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n---------------- [四項週指標精算結果] ----------------")
    print(f"(1) 走心留言數 (daily_interaction_limits.json) : {m1_count} 則")
    print(f"(2) 得到對方回覆數 (activity_replies_log.json) : {m2_count} 則 (同留言被回多次算 1)")
    print(f"(3) 回訪留言人數 (API conversation >=10字去重) : {m3_count} 人")
    print(f"(4) 熟稔常客人數 (friend_ledger 僅計留言/回覆 >=2 次，不計按讚) :")
    print(f"    - 累計熟客數     : {m4_cumulative_count} 人")
    print(f"    - 本週新增熟客數 : {m4_new_count} 人")
    print("------------------------------------------------------")
    print(f"💾 完整報表已寫入: {WEEKLY_REPORT_FILE.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
