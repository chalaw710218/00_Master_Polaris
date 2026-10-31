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

print("🔍 [看家門・留言掃描] 正在檢查近期貼文之所有網友留言...")

recent_post_ids = [
    "18121653928917604", # 昨晚小編便服入鏡露臉文
    "18637505857005596", # 昨天中午大太陽食氣昏睡文
    "18117857225104496"  # 前天傍晚東北季風立冬備戰文
]

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
