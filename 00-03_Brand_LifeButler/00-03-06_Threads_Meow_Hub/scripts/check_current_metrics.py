import sys
import requests
from pathlib import Path

cur = Path.cwd()
env_file = None
for p in [cur] + list(cur.parents):
    c = p / ".secrets.env"
    if c.exists():
        env_file = c
        break

env = {}
if env_file:
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()

token = env.get("THREADS_ACCESS_TOKEN")
uid = env.get("THREADS_USER_ID")

# 1. followers & profile views
url = f"https://graph.threads.net/v1.0/me/threads_insights?metric=views,followers_count&access_token={token}"
r = requests.get(url, timeout=15)
print("Account insights:", r.json())

# 2. user profile
u_url = f"https://graph.threads.net/v1.0/me?fields=id,username,threads_profile_picture_url,threads_biography&access_token={token}"
r2 = requests.get(u_url, timeout=15)
print("Profile:", r2.json())
