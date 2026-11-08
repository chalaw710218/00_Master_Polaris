import os
import sys
import json
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".secrets.env"
SCRIPT_DIR = Path(__file__).resolve().parent
STATE_FILE = SCRIPT_DIR / "replied_ids.json"

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

replied_ids = set()
if STATE_FILE.exists():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            replied_ids = set(json.load(f))
    except Exception:
        pass

print("🔍 [看家門・留言掃描] 正在從 Meta API 動態拉取最新貼文清單...")

# 徹底剷除寫死 ID：動態調用 API 取得最近 15 篇貼文
recent_post_ids = []
try:
    threads_url = f"{API_BASE}/{USER_ID}/threads?fields=id,text,permalink,timestamp&limit=15&access_token={TOKEN}"
    t_res = requests.get(threads_url, timeout=20).json()
    post_items = t_res.get("data", [])
    recent_post_ids = [item["id"] for item in post_items if "id" in item]
    print(f"📡 成功動態獲取最近 {len(recent_post_ids)} 篇貼文，準備逐篇掃描留言...")
except Exception as e:
    print(f"⚠️ 動態拉取貼文失敗: {e}，將使用備份機制")

unreplied_comments = []

for pid in recent_post_ids:
    url = f"{API_BASE}/{pid}/conversation?fields=id,text,timestamp,username,permalink&access_token={TOKEN}"
    try:
        r = requests.get(url, timeout=15).json()
        comments = r.get("data", [])
        for c in comments:
            cid = c.get("id")
            uname = c.get("username")
            # 排除自己發的回覆
            if uname == "hellotaitung":
                continue
            if cid not in replied_ids:
                print(f"🚨 發現未回覆留言！來自 @{uname} (ID: {cid})")
                print(f"   內容: {c.get('text')}")
                unreplied_comments.append({
                    "post_id": pid,
                    "comment_id": cid,
                    "username": uname,
                    "text": c.get("text"),
                    "permalink": c.get("permalink")
                })
            else:
                print(f"  ✓ @{uname} 的留言已回覆過 (ID: {cid})")
    except Exception as e:
        print(f"  ⚠️ 查詢貼文 {pid} 留言失敗: {e}")

if not unreplied_comments:
    print("\n✅ [看家門確認] 目前所有貼文下之網友留言均已 100% 回覆完畢，無任何遺漏！")
else:
    print(f"\n⚠️ 共有 {len(unreplied_comments)} 則留言待處理！")

with open(SCRIPT_DIR / "pending_comments.json", "w", encoding="utf-8") as f:
    json.dump(unreplied_comments, f, ensure_ascii=False, indent=2)
