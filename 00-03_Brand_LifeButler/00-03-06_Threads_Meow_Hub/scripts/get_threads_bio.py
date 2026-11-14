import sys
import os
import requests
import json
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

p = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.secrets.env")
env = {}
if p.exists():
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()

token = env.get("THREADS_ACCESS_TOKEN")
user_id = env.get("THREADS_USER_ID")

headers = {"Authorization": f"Bearer {token}"}
url = f"https://graph.threads.net/v1.0/{user_id}?fields=id,username,name,threads_profile_picture_url,threads_biography"

r = requests.get(url, headers=headers)
data = r.json()

print("=== THREADS PROFILE DATA ===")
print("Username:", data.get("username"))
print("Name:", data.get("name"))
print("Threads Biography:")
print(data.get("threads_biography"))
print("============================")
