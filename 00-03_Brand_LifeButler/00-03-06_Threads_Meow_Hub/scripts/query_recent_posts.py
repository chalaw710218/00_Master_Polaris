import os
import requests
import json

token = ""
env_path = os.path.join(os.path.dirname(__file__), "..", ".secrets.env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("THREADS_ACCESS_TOKEN="):
                token = line.strip().split("=", 1)[1].strip("\"'")

# Also check last few posts to see if there are other auction posts
url = "https://graph.threads.net/v1.0/me/threads?fields=id,text,timestamp,permalink&limit=10"
headers = {"Authorization": f"Bearer {token}"}
res = requests.get(url, headers=headers)
data = res.json()
with open("data/recent_posts_debug.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)

print("Saved recent posts to data/recent_posts_debug.json")
