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
# Query children or media_url
url = f"https://graph.threads.net/v1.0/{post_id}?fields=id,media_type,media_url,children{{id,media_type,media_url}}&access_token={token}"
res = requests.get(url, timeout=15).json()

print(json.dumps(res, ensure_ascii=False, indent=2))

save_dir = hub_dir / "images" / "auction_items_20261116"
save_dir.mkdir(parents=True, exist_ok=True)

downloaded = []
if "children" in res and "data" in res["children"]:
    for i, child in enumerate(res["children"]["data"]):
        m_url = child.get("media_url")
        if m_url:
            img_res = requests.get(m_url, timeout=30)
            file_name = f"auction_item_{i+1}_{child['id']}.jpg"
            file_path = save_dir / file_name
            with open(file_path, "wb") as f:
                f.write(img_res.content)
            downloaded.append(str(file_path))
elif res.get("media_url"):
    m_url = res["media_url"]
    img_res = requests.get(m_url, timeout=30)
    file_name = f"auction_single_{post_id}.jpg"
    file_path = save_dir / file_name
    with open(file_path, "wb") as f:
        f.write(img_res.content)
    downloaded.append(str(file_path))

print(f"Downloaded {len(downloaded)} images to {save_dir}")
for p in downloaded:
    print("-", p)
