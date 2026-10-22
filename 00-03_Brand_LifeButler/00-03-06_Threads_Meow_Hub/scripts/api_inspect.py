import sys
import requests
import json
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Find .secrets.env
cur = Path.cwd()
env_file = None
for p in [cur] + list(cur.parents):
    candidate = p / ".secrets.env"
    if candidate.exists():
        env_file = candidate
        break

env_vars = {}
if env_file:
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()

token = env_vars.get("THREADS_ACCESS_TOKEN")
user_id = env_vars.get("THREADS_USER_ID")

headers = {"Authorization": f"Bearer {token}"}

# Query user's recent threads
r = requests.get(f"https://graph.threads.net/v1.0/{user_id}/threads?fields=id,text,permalink,timestamp&limit=5", headers=headers)
data = r.json()
threads = data.get("data", [])
print(f"Total threads returned: {len(threads)}")

for t in threads:
    tid = t.get("id")
    permalink = t.get("permalink")
    text = t.get("text", "")
    ts = t.get("timestamp")
    print(f"\n==========================================")
    print(f"Thread ID: {tid} ({permalink}) [{ts}]")
    print(f"Content: {text[:100]}...")
    
    # Check conversation / replies
    r_conv = requests.get(f"https://graph.threads.net/v1.0/{tid}/conversation?fields=id,text,username,timestamp", headers=headers)
    replies = r_conv.json().get("data", [])
    print(f"💬 Replies ({len(replies)}):")
    for rep in replies:
        print(f"   - [@{rep.get('username')}] ({rep.get('timestamp')}): {rep.get('text')}")
