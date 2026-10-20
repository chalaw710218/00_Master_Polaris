import os
import sys
import time
import requests
from pathlib import Path

# 確保 Windows 支援 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".secrets.env"
ARCHIVE_PATH = Path(__file__).resolve().parent.parent / "03_Published_Archive.md"

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
API_BASE = "https://graph.threads.net/v1.0"

def get_post_insights(post_id):
    """取得單篇 Threads 貼文的即時成效指標"""
    if not TOKEN:
        print("❌ 缺少 THREADS_ACCESS_TOKEN")
        return None

    url = f"{API_BASE}/{post_id}/insights"
    params = {
        "metric": "views,likes,replies,reposts,quotes",
        "access_token": TOKEN
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print(f"⚠️ 讀取成效失敗 ({post_id}):", r.json())
        return None

    metrics = {}
    data = r.json().get("data", [])
    for item in data:
        name = item.get("name")
        values = item.get("values", [{}])
        val = values[0].get("value", 0) if values else 0
        metrics[name] = val
    return metrics

def get_account_insights():
    """取得帳號級別即時指標：粉絲數、個人檔案瀏覽數等"""
    if not TOKEN:
        print("❌ 缺少 THREADS_ACCESS_TOKEN")
        return None

    # 1. 抓取基本 Profile
    url_user = f"{API_BASE}/me?fields=id,username,name,threads_profile_picture_url,threads_biography&access_token={TOKEN}"
    r_user = requests.get(url_user).json()

    # 2. 抓取帳號級別 Insights
    url_insights = f"{API_BASE}/me/threads_insights?metric=views,likes,replies,reposts,quotes,followers_count&access_token={TOKEN}"
    r_insights = requests.get(url_insights).json()

    followers = 0
    profile_views_today = 0
    for item in r_insights.get("data", []):
        if item.get("name") == "followers_count":
            followers = item.get("total_value", {}).get("value", 0)
        elif item.get("name") == "views":
            vals = item.get("values", [])
            if vals:
                profile_views_today = vals[-1].get("value", 0)

    return {
        "username": r_user.get("username", "hellotaitung"),
        "name": r_user.get("name", ""),
        "followers_count": followers,
        "profile_views_today": profile_views_today
    }

def update_published_archive():
    """自動掃描帳號指標與已發布貼文成效"""
    print("🔍 [影的戰況雷達] 正在抓取 Threads 帳號與貼文真實成效...\n")

    acc = get_account_insights()
    if acc:
        print(f"👤 【帳號全貌】: @{acc['username']} ({acc['name']})")
        print(f"👥 【目前追蹤數 (Followers)】: {acc['followers_count']} 人")
        print(f"👀 【今日個人檔案瀏覽 (Profile Views)】: {acc['profile_views_today']} 次\n")

    tracked_posts = [
        {"id": "18114873908593734", "title": "【剛發布】煎午仔魚高麗菜那桌 🐟🥬🔥"},
        {"id": "18382679092238383", "title": "【附圖首發】日本氣象廳高壞球篇 ⚾🌪️🖼️"},
        {"id": "18467680978184165", "title": "【純文字測試】日本氣象廳高壞球篇 ⚾🌪️"}
    ]

    results = {}
    print("📜 【貼文即時成效盤點】:")
    for p in tracked_posts:
        pid = p["id"]
        res = get_post_insights(pid)
        if res:
            results[pid] = res
            print(f"📊 {p['title']}")
            print(f"   ↳ 瀏覽 {res.get('views', 0)} 次 | 按讚 {res.get('likes', 0)} | 留言 {res.get('replies', 0)} | 轉發 {res.get('reposts', 0)} | 引用 {res.get('quotes', 0)}")
            print(f"   ↳ 連結: https://www.threads.net/@hellotaitung/post/{pid}\n")

    return results

if __name__ == "__main__":
    update_published_archive()

