import sys
import json
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def load_env(env_path):
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env_vars[k.strip()] = v.strip()
    return env_vars

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV = load_env(ROOT_DIR / '.secrets.env')
TOKEN = ENV.get('THREADS_ACCESS_TOKEN')
USER_ID = ENV.get('THREADS_USER_ID')
API_BASE = 'https://graph.threads.net/v1.0'

SCRIPT_DIR = Path(__file__).resolve().parent
STATE_FILE = SCRIPT_DIR / "replied_ids.json"
replied_ids = set()
if STATE_FILE.exists():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            replied_ids = set(json.load(f))
    except Exception:
        pass

print("🔍 [看家門・夜巡掃描] 正在檢查最新 15 篇貼文之網友留言...")

url = f'{API_BASE}/me/threads?fields=id,text,permalink,timestamp&limit=15&access_token={TOKEN}'
res = requests.get(url).json()
posts = res.get('data', [])

unreplied = []

for p in posts:
    pid = p['id']
    curl = f'{API_BASE}/{pid}/conversation?fields=id,text,timestamp,username,permalink&access_token={TOKEN}'
    cres = requests.get(curl).json()
    cdata = cres.get('data', [])
    for c in cdata:
        cid = c.get('id')
        uname = c.get('username')
        if uname == 'hellotaitung':
            continue
        if cid not in replied_ids:
            print(f"🚨 發現未回覆留言！來自 @{uname} (ID: {cid})")
            print(f"   貼文: {p.get('text', '')[:30].replace(chr(10), ' ')}")
            print(f"   留言內容: {c.get('text')}")
            unreplied.append({
                "post_id": pid,
                "comment_id": cid,
                "username": uname,
                "text": c.get("text"),
                "permalink": c.get("permalink")
            })
        else:
            print(f"  ✓ @{uname} 的留言已回覆過 (ID: {cid})")

if not unreplied:
    print("\n✅ [看家門確認] 巡檢完畢！所有網友留言均已 100% 回覆完畢，無任何遺漏！")
else:
    print(f"\n⚠️ 共有 {len(unreplied)} 則留言待處理！")

with open(SCRIPT_DIR / "pending_comments.json", "w", encoding="utf-8") as f:
    json.dump(unreplied, f, ensure_ascii=False, indent=2)
