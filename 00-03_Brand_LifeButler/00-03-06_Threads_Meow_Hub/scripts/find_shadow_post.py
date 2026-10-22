import sys
import requests
import json
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

cur = Path.cwd()
env_file = None
for p in [cur] + list(cur.parents):
    candidate = p / ".secrets.env"
    if candidate.exists():
        env_file = candidate
        break

env_vars = {}
with open(env_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

token = env_vars.get("THREADS_ACCESS_TOKEN")
user_id = env_vars.get("THREADS_USER_ID")
headers = {"Authorization": f"Bearer {token}"}

# Query with limit=20
r = requests.get(f"https://graph.threads.net/v1.0/{user_id}/threads?fields=id,text,permalink,timestamp&limit=20", headers=headers)
data = r.json()
threads = data.get("data", [])
print(f"Total threads fetched: {len(threads)}")

for t in threads:
    tid = t.get("id")
    text = t.get("text", "")
    permalink = t.get("permalink")
    if "外星" in text or "板正" in text or "好啦" in text:
        print(f"\n🎯 找到目標貼文: {tid} ({permalink})")
        print(f"內文: {text[:80]}...")
        # Check replies
        r_conv = requests.get(f"https://graph.threads.net/v1.0/{tid}/conversation?fields=id,text,username,timestamp", headers=headers)
        replies = r_conv.json().get("data", [])
        print(f"Replies ({len(replies)}):")
        for rep in replies:
            print(f"  Comment ID: {rep.get('id')}")
            print(f"  Author: @{rep.get('username')}")
            print(f"  Content: {rep.get('text')}")
