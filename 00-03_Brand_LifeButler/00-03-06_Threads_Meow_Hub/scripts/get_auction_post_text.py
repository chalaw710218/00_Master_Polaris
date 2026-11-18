import os
import sys
from pathlib import Path
import requests
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

hub_dir = Path(".").resolve()
root_dir = hub_dir.parents[1]
env_path = root_dir / ".secrets.env"

token = ""
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("THREADS_ACCESS_TOKEN="):
                token = line.strip().split("=", 1)[1].strip("\"'")

post_id = "18150791674564224"
url = f"https://graph.threads.net/v1.0/{post_id}?fields=id,text,timestamp,permalink,media_type&access_token={token}"
res = requests.get(url, timeout=15).json()

with open("data/auction_post_detail.json", "w", encoding="utf-8") as out:
    json.dump(res, out, ensure_ascii=False, indent=2)

print("SUCCESS: Post text fetched:")
print(res.get("text", "No text"))
