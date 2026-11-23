#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polaris Threads Interaction Safety Gate (社群互動安全節奏與防風控門禁)
作者: 影 (Shadow · 首席特務兼生活管家)

嚴格把關帳號安全，避免高頻自動化被 Meta 判定為機器人：
1. 每日走心留言上限: 15 則
2. 每日愛心點讚上限: 60 個
3. 連續留言間隔: 至少 120 秒 (強制冷卻倒數)
4. 逛逛啟動時間去規律化 (Jitter: 避開整點)
5. 狀態即時持久化至 data/daily_interaction_limits.json
"""

import sys
import json
import time
import random
from pathlib import Path
from datetime import datetime, date

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LIMITS_FILE = DATA_DIR / "daily_interaction_limits.json"

# 法定預設防護參數
DEFAULT_MAX_COMMENTS = 15
DEFAULT_MAX_LIKES = 60
DEFAULT_MIN_COMMENT_INTERVAL = 120  # 秒


def _get_today_str() -> str:
    return date.today().isoformat()


def load_safety_state(max_comments: int = None, max_likes: int = None) -> dict:
    """載入今日安全計數狀態，若跨日則自動輪替重置"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = _get_today_str()

    default_mc = max_comments if max_comments is not None else DEFAULT_MAX_COMMENTS
    default_ml = max_likes if max_likes is not None else DEFAULT_MAX_LIKES

    state = {
        "date": today,
        "max_comments": default_mc,
        "max_likes": default_ml,
        "min_comment_interval_seconds": DEFAULT_MIN_COMMENT_INTERVAL,
        "comments_count": 0,
        "likes_count": 0,
        "last_comment_timestamp": 0,
        "history": []
    }

    if LIMITS_FILE.exists():
        try:
            with open(LIMITS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                if saved.get("date") == today:
                    state = saved
                    if max_comments is not None:
                        state["max_comments"] = max_comments
                    if max_likes is not None:
                        state["max_likes"] = max_likes
                else:
                    # 每日 0 點跨日自動歸零當日計數器，並保留 history 供週報統計
                    state["date"] = today
                    state["comments_count"] = 0
                    state["likes_count"] = 0
                    state["last_comment_timestamp"] = saved.get("last_comment_timestamp", 0)
                    state["history"] = saved.get("history", [])
                    save_safety_state(state)
        except Exception as e:
            err_msg = (
                f"🚨 [安全門禁讀檔失敗] 無法讀取或解析 {LIMITS_FILE}: {e}。"
                f"已硬性停止執行，嚴禁覆蓋原檔案以保護 history 紀錄！"
            )
            print(err_msg, file=sys.stderr, flush=True)
            raise RuntimeError(err_msg) from e
    else:
        save_safety_state(state)

    return state


def save_safety_state(state: dict):
    """持久化狀態入庫"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(LIMITS_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def can_comment(max_comments: int = None) -> tuple[bool, str]:
    """
    檢查是否允許發送走心留言
    返回 (是否允許, 原因說明)
    """
    state = load_safety_state()
    max_c = max_comments if max_comments is not None else state.get("max_comments", DEFAULT_MAX_COMMENTS)
    count = state.get("comments_count", 0)

    if count >= max_c:
        msg = f"已達今日走心留言安全上限 ({count}/{max_c})，自動停止留言"
        return False, msg

    return True, f"目前留言計數: {count}/{max_c}，在安全額度內"


def wait_comment_cooldown(min_interval: int = DEFAULT_MIN_COMMENT_INTERVAL):
    """
    強制執行留言安全冷卻間隔 (預設 120 秒)
    """
    state = load_safety_state()
    last_ts = state.get("last_comment_timestamp", 0)
    if last_ts > 0:
        elapsed = time.time() - last_ts
        if elapsed < min_interval:
            wait_sec = int(min_interval - elapsed) + 1
            print(f"   ⏳ [防風控冷卻] 距上次留言僅 {int(elapsed)} 秒，安全冷卻等待 {wait_sec} 秒...", flush=True)
            time.sleep(wait_sec)


def record_comment(target_user: str, post_url: str = "", comment_text: str = "", max_comments: int = None):
    """
    登記一則成功發送的走心留言，並寫入紀錄
    """
    state = load_safety_state(max_comments=max_comments)
    state["comments_count"] = state.get("comments_count", 0) + 1
    state["last_comment_timestamp"] = time.time()

    item = {
        "timestamp": datetime.now().isoformat(),
        "type": "comment",
        "target_user": target_user.lstrip("@"),
        "post_url": post_url,
        "comment_text": comment_text[:100]
    }
    state.setdefault("history", []).append(item)
    save_safety_state(state)
    print(f"   📊 [安全計數更新] 今日走心留言: {state['comments_count']}/{state['max_comments']}", flush=True)


def can_like(max_likes: int = None) -> tuple[bool, str]:
    """
    檢查是否允許按愛心
    返回 (是否允許, 原因說明)
    """
    state = load_safety_state()
    max_l = max_likes if max_likes is not None else state.get("max_likes", DEFAULT_MAX_LIKES)
    count = state.get("likes_count", 0)

    if count >= max_l:
        msg = f"已達今日愛心點讚安全上限 ({count}/{max_l})，自動停止按讚"
        return False, msg

    return True, f"目前按讚計數: {count}/{max_l}，在安全額度內"


def record_like(target_user: str = "", post_url: str = "", max_likes: int = None):
    """
    登記一次成功點讚，並寫入紀錄
    """
    state = load_safety_state(max_likes=max_likes)
    state["likes_count"] = state.get("likes_count", 0) + 1

    item = {
        "timestamp": datetime.now().isoformat(),
        "type": "like",
        "target_user": target_user.lstrip("@"),
        "post_url": post_url
    }
    state.setdefault("history", []).append(item)
    save_safety_state(state)
    print(f"   ❤️ [安全計數更新] 今日愛心點讚: {state['likes_count']}/{state['max_likes']}", flush=True)


def apply_walk_jitter(force_check: bool = False):
    """
    去規律化 Jitter：避免在整點 (如 XX:00) 瞬間啟動漫遊
    如果當前分鐘為 00, 01, 02，隨機偏移等待 60~180 秒
    """
    now = datetime.now()
    if force_check or now.minute in (0, 1, 2):
        jitter_sec = random.randint(60, 180)
        print(f"   🎲 [啟動時間 Jitter] 當前時間接近整點 ({now.strftime('%H:%M')})，隨機偏移 {jitter_sec} 秒以消除機器人規律特徵...", flush=True)
        time.sleep(jitter_sec)


def reset_daily_stats_for_test(max_comments: int = DEFAULT_MAX_COMMENTS, max_likes: int = DEFAULT_MAX_LIKES):
    """重置計數器狀態（供測試與校準使用）"""
    state = {
        "date": _get_today_str(),
        "max_comments": max_comments,
        "max_likes": max_likes,
        "min_comment_interval_seconds": DEFAULT_MIN_COMMENT_INTERVAL,
        "comments_count": 0,
        "likes_count": 0,
        "last_comment_timestamp": 0,
        "history": []
    }
    save_safety_state(state)
    return state


if __name__ == "__main__":
    state = load_safety_state()
    print("=== Threads 互動安全門禁儀表板 ===")
    print(f"日期: {state['date']}")
    print(f"今日走心留言: {state['comments_count']} / {state['max_comments']}")
    print(f"今日愛心點讚: {state['likes_count']} / {state['max_likes']}")
    print(f"留言冷卻間隔: {state['min_comment_interval_seconds']} 秒")
